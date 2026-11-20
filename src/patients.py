"""Persistência de perfis e evolução FICTÍCIOS para demonstração acadêmica.

A seleção do papel em Streamlit NÃO autentica nem autoriza usuários.
Nunca armazenar prontuários identificáveis neste módulo demonstrativo.
"""

import json
from contextlib import contextmanager
import os
import sqlite3
import uuid
from datetime import date, datetime, timezone
from pathlib import Path


DEMO_PATIENT_ID = "DEMO-001"
_ALLOWED_NOTE_TYPES = ("Observação", "Pendência", "Plano de acompanhamento")
_ALLOWED_ORIGINS = ("Paciente demonstrativo", "Médico demonstrativo")
_FIELDS = ("glicemia_jejum", "hba1c", "ttgo_1h", "ttgo_2h", "glicemia_casual")


def _path():
    return Path(os.environ.get("FUNDAMENTO_DEMO_DB", str(Path(__file__).resolve().parents[1] / "runtime" / "demo.sqlite")))


def _conn():
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con


@contextmanager
def _db():
    con = _conn()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def initialize_demo():
    """Cria o esquema e os pacientes fictícios sem duplicar registros."""
    with _db() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS demo_patients (
              id TEXT PRIMARY KEY, label TEXT NOT NULL, age INTEGER NOT NULL,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS demo_exams (
              id TEXT PRIMARY KEY, patient_id TEXT NOT NULL REFERENCES demo_patients(id),
              examined_on TEXT NOT NULL, recorded_at TEXT NOT NULL,
              recorded_by TEXT NOT NULL, values_json TEXT NOT NULL,
              conditions_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_demo_exams_patient
                ON demo_exams(patient_id, examined_on DESC);
            CREATE TABLE IF NOT EXISTS demo_notes (
              id TEXT PRIMARY KEY, patient_id TEXT NOT NULL REFERENCES demo_patients(id),
              created_at TEXT NOT NULL, author TEXT NOT NULL, type TEXT NOT NULL,
              body TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_demo_notes_patient
                ON demo_notes(patient_id, created_at DESC);
        """)
        now = "2026-11-20T12:00:00+00:00"
        patients = [("DEMO-001", "Paciente fictício 001", 58, now),
                    ("DEMO-002", "Paciente fictício 002", 44, now)]
        con.executemany("INSERT OR IGNORE INTO demo_patients VALUES (?,?,?,?)", patients)
        fixtures = [
            ("EX-001-A", "DEMO-001", "2026-03-10", "Paciente demonstrativo", {"glicemia_jejum": 104, "hba1c": 5.8}),
            ("EX-001-B", "DEMO-001", "2026-07-18", "Paciente demonstrativo", {"glicemia_jejum": 115, "hba1c": 6.1}),
            ("EX-001-C", "DEMO-001", "2026-11-12", "Paciente demonstrativo", {"glicemia_jejum": 132, "hba1c": 6.8}),
            ("EX-002-A", "DEMO-002", "2026-11-08", "Paciente demonstrativo", {"glicemia_jejum": 91, "hba1c": 5.4}),
        ]
        defaults = {"adult": True, "pregnant": False, "known_diabetes": False,
                    "fasting_confirmed": True, "ogtt_75g_confirmed": True,
                    "certified_a1c": True, "a1c_interference": False,
                    "classic_symptoms": False}
        con.executemany("INSERT OR IGNORE INTO demo_exams VALUES (?,?,?,?,?,?,?)", [
            (eid, pid, d, now, role, json.dumps(vals), json.dumps(defaults))
            for eid, pid, d, role, vals in fixtures
        ])
        con.execute("INSERT OR IGNORE INTO demo_notes VALUES (?,?,?,?,?,?)", (
            "NOTE-001", "DEMO-001", "2026-11-13T14:00:00+00:00", "Médico demonstrativo",
            "Pendência", "Nota inteiramente fictícia: conferir condições de coleta e revisar evolução de HbA1c."
        ))


def list_patients():
    with _db() as con:
        return [dict(r) for r in con.execute("SELECT * FROM demo_patients ORDER BY id")]


def get_patient(patient_id):
    with _db() as con:
        r = con.execute("SELECT * FROM demo_patients WHERE id=?", (patient_id,)).fetchone()
        return dict(r) if r else None


def add_patient(label, age):
    if not isinstance(label, str) or not 3 <= len(label.strip()) <= 60:
        raise ValueError("Identificação fictícia deve ter 3 a 60 caracteres.")
    if not isinstance(age, int) or not 18 <= age <= 110:
        raise ValueError("A demonstração contempla adultos entre 18 e 110 anos.")
    pid = "DEMO-" + uuid.uuid4().hex[:8].upper()
    with _db() as con:
        con.execute("INSERT INTO demo_patients VALUES (?,?,?,?)", (
            pid, label.strip(), age, datetime.now(timezone.utc).isoformat()))
    return pid


def _require_patient(con, patient_id):
    if not con.execute("SELECT 1 FROM demo_patients WHERE id=?", (patient_id,)).fetchone():
        raise ValueError("Paciente fictício não encontrado.")


def add_exam(patient_id, examined_on, values, conditions, recorded_by):
    from src.clinical import evaluate_labs, _num
    if recorded_by not in _ALLOWED_ORIGINS:
        raise ValueError("Origem inválida.")
    try:
        d = date.fromisoformat(str(examined_on))
    except ValueError:
        raise ValueError("Data de exame inválida.") from None
    if d > date.today():
        raise ValueError("A data do exame não pode estar no futuro.")
    if not isinstance(values, dict) or any(k not in _FIELDS for k in values):
        raise ValueError("Campos de exame inválidos.")
    if not isinstance(conditions, dict):
        raise ValueError("Condições de exame inválidas.")
    allowed = {"adult", "pregnant", "known_diabetes", "fasting_confirmed",
               "ogtt_75g_confirmed", "certified_a1c", "a1c_interference", "classic_symptoms"}
    if any(k not in allowed or not isinstance(v, bool) for k,v in conditions.items()):
        raise ValueError("Condições de exame inválidas.")
    filled = {k: v for k,v in values.items() if v not in (None, '')}
    if not filled:
        raise ValueError("Informe pelo menos um exame antes de salvar.")
    for key, value in filled.items():
        _num(key, value)  # valida também valores de perfis fora do escopo automático
    evaluate_labs(values, **conditions)  # preserva as verificações clínicas atuais
    canonical_values = {k: None for k in _FIELDS}
    for key in _FIELDS:
        if values.get(key) not in (None, ""):
            canonical_values[key] = float(str(values[key]).replace(",", "."))
    rid = uuid.uuid4().hex
    with _db() as con:
        _require_patient(con, patient_id)
        con.execute("INSERT INTO demo_exams VALUES (?,?,?,?,?,?,?)", (
            rid, patient_id, d.isoformat(), datetime.now(timezone.utc).isoformat(),
            recorded_by, json.dumps(canonical_values, allow_nan=False),
            json.dumps(conditions, allow_nan=False)))
    return rid


def list_exams(patient_id):
    with _db() as con:
        _require_patient(con, patient_id)
        rows = con.execute(
            "SELECT * FROM demo_exams WHERE patient_id=? ORDER BY examined_on DESC, recorded_at DESC",
            (patient_id,)).fetchall()
    return [{**dict(r), "values": json.loads(r["values_json"]),
             "conditions": json.loads(r["conditions_json"])} for r in rows]


def add_note(patient_id, author, note_type, body):
    if author != "Médico demonstrativo":
        raise ValueError("Somente o papel de médico demonstrativo registra notas.")
    if note_type not in _ALLOWED_NOTE_TYPES:
        raise ValueError("Tipo de nota inválido.")
    if not isinstance(body, str) or not 5 <= len(body.strip()) <= 1000:
        raise ValueError("A observação deve ter de 5 a 1000 caracteres.")
    rid = uuid.uuid4().hex
    with _db() as con:
        _require_patient(con, patient_id)
        con.execute("INSERT INTO demo_notes VALUES (?,?,?,?,?,?)", (
            rid, patient_id, datetime.now(timezone.utc).isoformat(), author,
            note_type, body.strip()))
    return rid


def list_notes(patient_id):
    with _db() as con:
        _require_patient(con, patient_id)
        return [dict(r) for r in con.execute(
            "SELECT * FROM demo_notes WHERE patient_id=? ORDER BY created_at DESC", (patient_id,))]
