"""Identificação local de contas FICTÍCIAS no protótipo acadêmico.

Demonstra uma separação de telas, mas NÃO é autenticação pronta para
prontuários reais, internet pública ou tratamento de dados pessoais.
Os segredos são criados aleatoriamente e escritos somente no ambiente local.
"""

import hashlib
import hmac
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path

from src.patients import _db, _path

ITERATIONS = 260_000
DEMO_LOGINS = (
    ("MED-DEMO", "doctor", None),
    ("MED-002", "doctor", None),
    ("DEMO-001", "patient", "DEMO-001"),
    ("DEMO-002", "patient", "DEMO-002"),
)


def _digest(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)


def _new_secret() -> str:
    return secrets.token_urlsafe(18)


def _create_account(con, login: str, role: str, patient_id: str | None, password: str):
    salt = os.urandom(16)
    con.execute("""INSERT INTO demo_accounts
                 (login, role, patient_id, salt, password_hash, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)""",
                (login, role, patient_id, salt, _digest(password, salt),
                 datetime.now(timezone.utc).isoformat()))


def initialize_auth():
    """Primeiro início: cria contas e gera credenciais em arquivo local ignorado pelo Git.

    A rotina é idempotente. Se o arquivo for apagado, a senha não pode ser lida
    do banco; use `python -m src.auth reset <LOGIN>` para gerar outra.
    """
    issued = []
    with _db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS demo_accounts (
            login TEXT PRIMARY KEY,
            role TEXT NOT NULL CHECK (role IN ('doctor', 'patient')),
            patient_id TEXT REFERENCES demo_patients(id),
            salt BLOB NOT NULL,
            password_hash BLOB NOT NULL,
            created_at TEXT NOT NULL
        )""")
        for login, role, pid in DEMO_LOGINS:
            if not con.execute("SELECT 1 FROM demo_accounts WHERE login=?", (login,)).fetchone():
                password = _new_secret()
                _create_account(con, login, role, pid, password)
                issued.append((login, password))
    if issued:
        target = _path().parent / "ACESSOS_DEMONSTRACAO.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        # O_EXCL evita sobrescrever senhas anteriores e permite permissão restrita.
        try:
            fd = os.open(str(target), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            # Em projeto já inicializado com o arquivo preservado, não acrescentar
            # senhas em texto claro. Administrador local pode redefini-las pelo CLI.
            pass
        else:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                file.write("SOMENTE DEMONSTRACAO LOCAL, COM PACIENTES FICTICIOS.\n"
                           "NAO PUBLICAR NEM COMPARTILHAR ESSE ARQUIVO.\n\n")
                for login, password in issued:
                    file.write(f"Perfil: {login}\nSenha: {password}\n\n")
    return bool(issued)


def authenticate(login: str, password: str):
    """Retorna identidade básica ou None; nunca retorna o hash ou a senha."""
    if not isinstance(login, str) or not isinstance(password, str):
        return None
    login = login.strip().upper()
    if not login or not password or len(login) > 80 or len(password) > 512:
        return None
    with _db() as con:
        row = con.execute("SELECT * FROM demo_accounts WHERE login=?", (login,)).fetchone()
    if row is None:
        # Trabalho constante aproximado para reduzir descoberta de contas.
        hmac.compare_digest(_digest(password, b"0" * 16), b"0" * 32)
        return None
    if not hmac.compare_digest(_digest(password, row["salt"]), row["password_hash"]):
        return None
    return {"login": row["login"], "role": row["role"], "patient_id": row["patient_id"]}


def can_view_profile(account: dict, patient_id: str) -> bool:
    """Condição de acesso demonstrativo, usada pelas telas do portal."""
    return bool(isinstance(account, dict) and (
        account.get("role") == "doctor" or
        (account.get("role") == "patient" and account.get("patient_id") == patient_id)
    ))


def can_edit_profile(account: dict, patient_id: str) -> bool:
    return bool(isinstance(account, dict) and account.get("role") == "doctor"
                and isinstance(patient_id, str) and patient_id.startswith("DEMO-"))


def create_patient_login(patient_id: str):
    """Cria credencial de um perfil fictício; senha exibida apenas uma vez."""
    if not isinstance(patient_id, str) or not patient_id.startswith("DEMO-"):
        raise ValueError("Identificação fictícia inválida.")
    password = _new_secret()
    with _db() as con:
        if not con.execute("SELECT 1 FROM demo_patients WHERE id=?", (patient_id,)).fetchone():
            raise ValueError("Paciente fictício não encontrado.")
        if con.execute("SELECT 1 FROM demo_accounts WHERE login=?", (patient_id,)).fetchone():
            raise ValueError("Já existe uma conta para este paciente.")
        _create_account(con, patient_id, "patient", patient_id, password)
    return password


def reset_password_local(login: str):
    """Administração CLI local, não exposta na interface."""
    login = login.strip().upper()
    password = _new_secret()
    salt = os.urandom(16)
    with _db() as con:
        result = con.execute("""UPDATE demo_accounts SET salt=?, password_hash=?
                                WHERE login=?""", (salt, _digest(password, salt), login))
        if result.rowcount != 1:
            raise ValueError("Conta fictícia inexistente.")
    return password


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gerenciar credenciais FICTÍCIAS locais")
    parser.add_argument("action", choices=["reset"])
    parser.add_argument("login", help="MED-DEMO, DEMO-001 ou outro login cadastrado")
    args = parser.parse_args()
    print(f"Perfil: {args.login.upper()}\nNova senha: {reset_password_local(args.login)}")
