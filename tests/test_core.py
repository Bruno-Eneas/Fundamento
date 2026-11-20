import os, sqlite3, tempfile, unittest
from src.core import CASES, explain, retrieve, validate, validate_generated
from src.storage import save_feedback


class CoreTests(unittest.TestCase):
    def test_shap_reconstruction(self):
        for v in CASES.values():
            r = explain(v)
            self.assertAlmostEqual(
                r["base"] + sum(x["contribution"] for x in r["factors"]),
                r["score"],
                places=7,
            )
            self.assertTrue(0 <= r["score"] <= 1)

    def test_missing_and_invalid(self):
        for updates in [
            {"BMI": None},
            {"BMI": float("nan")},
            {"Age": 14},
            {"Age": 2.5},
            {"HighBP": 3},
        ]:
            with self.assertRaises(ValueError):
                validate({**next(iter(CASES.values())), **updates})

    def test_retrieval_and_abstention(self):
        for f in ["BMI", "Age", "PhysActivity"]:
            self.assertTrue(retrieve(f))
            self.assertTrue(all(f in d["features"] for d in retrieve(f)))
        self.assertEqual(retrieve("HighBP"), [])

    def test_false_citation_blocked(self):
        with self.assertRaises(ValueError):
            validate_generated(
                {"claims": [{"text": "Exemplo", "source_ids": ["inventada"]}]},
                retrieve("BMI"),
            )
        self.assertEqual(validate_generated({"claims": []}, []), [])

    def test_generation_limits_reject_unbounded_or_repeated_citations(self):
        docs = retrieve("BMI")
        with self.assertRaises(ValueError):
            validate_generated(
                {"claims": [{"text": "a", "source_ids": [docs[0]["id"]]}] * 7},
                docs,
            )
        with self.assertRaises(ValueError):
            validate_generated(
                {"claims": [{"text": "a", "source_ids": [docs[0]["id"]] * 2}]},
                docs,
            )

    def test_feedback_survives_connection(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = os.environ.pop("DATABASE_URL", None)
            os.environ["FUNDAMENTO_DB"] = tmp + "/test.sqlite"
            try:
                rid = save_feedback({"case": "fictício"}, "Concordo", "Teste d'água")
                with sqlite3.connect(os.environ["FUNDAMENTO_DB"]) as c:
                    row = c.execute("SELECT id,comment FROM feedback").fetchone()
                self.assertEqual(row, (rid, "Teste d'água"))
            finally:
                os.environ.pop("FUNDAMENTO_DB", None)
                if old:
                    os.environ["DATABASE_URL"] = old


if __name__ == "__main__":
    unittest.main()
