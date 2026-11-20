import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.patients import initialize_demo, add_patient
from src.auth import initialize_auth, authenticate, create_patient_login, reset_password_local, can_view_profile, can_edit_profile
from src.presentation import brief_status
from src.clinical import evaluate_labs


class DemoAccessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {"FUNDAMENTO_DEMO_DB": self.tmp.name + "/demo.sqlite"})
        self.env.start()
        initialize_demo()
        initialize_auth()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def _credentials(self):
        text = Path(self.tmp.name, "ACESSOS_DEMONSTRACAO.txt").read_text(encoding="utf-8")
        lines = [line.strip() for line in text.splitlines()]
        return {lines[i].split(": ", 1)[1]: lines[i+1].split(": ", 1)[1]
                for i in range(len(lines)-1) if lines[i].startswith("Perfil: ")}

    def test_first_run_distinct_random_credentials(self):
        creds = self._credentials()
        self.assertEqual(set(creds), {"MED-DEMO", "MED-002", "DEMO-001", "DEMO-002"})
        self.assertEqual(len(set(creds.values())), 4)
        self.assertTrue(all(len(secret) >= 16 for secret in creds.values()))
        self.assertEqual(authenticate("med-demo", creds["MED-DEMO"])["role"], "doctor")
        self.assertEqual(authenticate("demo-002", creds["DEMO-002"])["patient_id"], "DEMO-002")
        self.assertIsNone(authenticate("DEMO-001", creds["DEMO-002"]))
        self.assertIsNone(authenticate("nonexistent", "secret"))
        self.assertIsNone(authenticate("MED-DEMO", ""))

    def test_auth_is_idempotent(self):
        creds = self._credentials()
        self.assertFalse(initialize_auth())
        self.assertTrue(authenticate("MED-DEMO", creds["MED-DEMO"]))

    def test_new_patient_credentials_and_reset(self):
        pid = add_patient("Paciente teste", 39)
        pwd = create_patient_login(pid)
        self.assertEqual(authenticate(pid, pwd)["patient_id"], pid)
        with self.assertRaises(ValueError):
            create_patient_login(pid)
        new = reset_password_local(pid)
        self.assertIsNone(authenticate(pid, pwd))
        self.assertIsNotNone(authenticate(pid, new))
        with self.assertRaises(ValueError):
            reset_password_local("DEMO-404")

    def test_role_scoping(self):
        p1 = {"role": "patient", "patient_id": "DEMO-001"}
        doctor = {"role": "doctor", "patient_id": None}
        self.assertTrue(can_view_profile(p1, "DEMO-001"))
        self.assertFalse(can_view_profile(p1, "DEMO-002"))
        self.assertFalse(can_edit_profile(p1, "DEMO-001"))
        self.assertTrue(can_view_profile(doctor, "DEMO-002"))
        self.assertTrue(can_edit_profile(doctor, "DEMO-001"))
        self.assertFalse(can_view_profile({}, "DEMO-001"))

    def test_patient_summary_has_no_false_diabetes_probability(self):
        result = evaluate_labs({"glicemia_jejum": 132, "hba1c": 6.8},
                               adult=True, fasting_confirmed=True, certified_a1c=True)
        summary = brief_status(result)
        self.assertEqual(summary["level"], "ALERTA")
        self.assertNotIn("%", str(summary))
        self.assertNotIn("tipo 2 confirmado", str(summary).lower())

    def test_patient_summary_preserves_uncertainty(self):
        result = evaluate_labs({"glicemia_jejum": 91}, fasting_confirmed=True)
        summary = brief_status(result)
        self.assertIn("não", summary["reason"].lower())

if __name__ == "__main__":
    unittest.main()
