import os
import unittest
from unittest.mock import patch
from src.showcase import mode, sample_account
from src.auth import can_view_profile, can_edit_profile


class ShowcaseTests(unittest.TestCase):
    def test_default_mode_is_off(self):
        with patch.dict(os.environ, {'FUNDAMENTO_PUBLIC_SHOWCASE': '0', 'FUNDAMENTO_PRESENTATION_MODE': '0'}):
            self.assertIsNone(mode())

    def test_local_is_explicit(self):
        with patch.dict(os.environ, {'FUNDAMENTO_PUBLIC_SHOWCASE': '', 'FUNDAMENTO_PRESENTATION_MODE': '1'}):
            self.assertEqual(mode(), 'local')

    def test_public_mode_precedes_local(self):
        with patch.dict(os.environ, {'FUNDAMENTO_PUBLIC_SHOWCASE': '1', 'FUNDAMENTO_PRESENTATION_MODE': '1'}):
            self.assertEqual(mode(), 'publico')

    def test_patient_account_is_scoped(self):
        account = sample_account('patient')
        self.assertTrue(can_view_profile(account, 'DEMO-001'))
        self.assertFalse(can_view_profile(account, 'DEMO-002'))
        self.assertFalse(can_edit_profile(account, 'DEMO-001'))

    def test_demo_doctor_role(self):
        self.assertTrue(can_view_profile(sample_account('doctor'), 'DEMO-002'))
        with self.assertRaises(ValueError):
            sample_account('administrator')


if __name__ == '__main__':
    unittest.main()
