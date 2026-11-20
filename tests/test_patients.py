import os
import tempfile
import unittest
from unittest.mock import patch
from src.patients import (
    DEMO_PATIENT_ID, initialize_demo, list_patients, get_patient, add_patient,
    add_exam, list_exams, add_note, list_notes,
)


class PatientsDemoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {"FUNDAMENTO_DEMO_DB": self.tmp.name + "/demo.sqlite"})
        self.env.start()
        initialize_demo()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_seed_idempotent(self):
        self.assertEqual(len(list_patients()), 2)
        self.assertEqual(len(list_exams(DEMO_PATIENT_ID)), 3)
        initialize_demo()
        self.assertEqual(len(list_exams(DEMO_PATIENT_ID)), 3)
        self.assertEqual(len(list_notes(DEMO_PATIENT_ID)), 1)

    def test_profile_and_record_history(self):
        pid = add_patient("Perfil teste fictício", 35)
        self.assertEqual(get_patient(pid)["age"], 35)
        rid = add_exam(pid, "2026-11-12", {"glicemia_jejum": 132, "hba1c": "6,8"},
                       {"adult": True, "fasting_confirmed": True, "certified_a1c": True},
                       "Paciente demonstrativo")
        self.assertEqual(list_exams(pid)[0]["id"], rid)
        self.assertEqual(list_exams(pid)[0]["values"]["hba1c"], 6.8)

    def test_reject_bad_exams(self):
        before = len(list_exams(DEMO_PATIENT_ID))
        for vals in [{"hba1c": "abc"}, {"hba1c": float('nan')}, {}]:
            with self.assertRaises(ValueError):
                add_exam(DEMO_PATIENT_ID, "2026-11-15", vals, {}, "Paciente demonstrativo")
        self.assertEqual(len(list_exams(DEMO_PATIENT_ID)), before)

    def test_notes_append_only_and_scope(self):
        before = len(list_notes(DEMO_PATIENT_ID))
        with self.assertRaises(ValueError):
            add_note(DEMO_PATIENT_ID, "Paciente demonstrativo", "Observação", "Nota inválida")
        rid = add_note(DEMO_PATIENT_ID, "Médico demonstrativo", "Observação", "Conferir exames fictícios.")
        notes = list_notes(DEMO_PATIENT_ID)
        self.assertEqual(len(notes), before + 1)
        self.assertEqual(notes[0]["id"], rid)
        self.assertEqual(list_notes("DEMO-002"), [])

    def test_unknown_patient_and_untrusted_label(self):
        with self.assertRaises(ValueError):
            list_exams("missing")
        with self.assertRaises(ValueError):
            add_note("missing", "Médico demonstrativo", "Observação", "Alguma observação")
        with self.assertRaises(ValueError):
            add_patient("xx", 35)

if __name__ == '__main__':
    unittest.main()
