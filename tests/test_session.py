import json
import unittest
from src.session import generate_result


class SessionTests(unittest.TestCase):
    def state(self):
        return {
            "result": {
                "factors": [{"feature": "BMI"}, {"feature": "Age"}],
                "retrieved": {"BMI": [{"id": "E02"}], "Age": [{"id": "E01"}]},
            }
        }

    def test_success_then_failure_clears_export(self):
        state = self.state()
        self.assertTrue(
            generate_result(
                state, lambda f, d: [{"text": "contexto", "source_ids": [d[0]["id"]]}]
            )
        )
        self.assertIn("generated_draft", state["result"])

        def fail(f, d):
            raise TimeoutError("offline")

        self.assertFalse(generate_result(state, fail))
        self.assertNotIn("generated_draft", json.loads(json.dumps(state["result"])))
        self.assertNotIn("generated", state)
        self.assertIn("generation_error", state)

    def test_partial_failure_is_atomic(self):
        state = self.state()

        def partial(f, d):
            if f["feature"] == "Age":
                raise ValueError("invalid")
            return [{"text": "primeiro", "source_ids": ["E02"]}]

        self.assertFalse(generate_result(state, partial))
        self.assertNotIn("generated_draft", state["result"])

    def test_no_evidence_does_not_call_generator(self):
        state = self.state()
        state["result"]["retrieved"] = {"BMI": [], "Age": []}

        def fail(f, d):
            raise AssertionError("não deve chamar")

        self.assertTrue(generate_result(state, fail))
        self.assertEqual(state["result"]["generated_draft"], {})
