import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from src.storage import save_feedback

class StorageTests(unittest.TestCase):
    def test_invalid_input_does_not_create_database(self):
        with tempfile.TemporaryDirectory() as temp:
            path = temp + '/feedback.sqlite'
            with patch.dict(os.environ, {'DATABASE_URL':'','FUNDAMENTO_DB':path}):
                for rating, comment in [(None,''), ('Concordo',None), ('Concordo','x'*501)]:
                    with self.assertRaises(ValueError): save_feedback({},rating,comment)
                self.assertFalse(os.path.exists(path))

    def test_nonfinite_payload_not_inserted(self):
        with tempfile.TemporaryDirectory() as temp:
            path=temp+'/feedback.sqlite'
            with patch.dict(os.environ, {'DATABASE_URL':'','FUNDAMENTO_DB':path}):
                with self.assertRaises(ValueError): save_feedback({'score':float('nan')},'Concordo','')
                with sqlite3.connect(path) as conn:
                    self.assertEqual(conn.execute('SELECT count(*) FROM feedback').fetchone()[0],0)
