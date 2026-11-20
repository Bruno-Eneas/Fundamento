import io
import json
import os
import unittest
from unittest.mock import patch
from src.generation import generate


class GenerationTests(unittest.TestCase):
    docs = [{"id": "E02", "summary": "contexto", "excerpt": "trecho"}]
    factor = {"label": "IMC"}

    def response(self, payload):
        return io.BytesIO(
            json.dumps({"message": {"content": json.dumps(payload)}}).encode()
        )

    def test_offline_returns_no_fake_text(self):
        with (
            patch.dict(os.environ, {"OLLAMA_MODEL": "qwen2.5:3b"}),
            patch("urllib.request.urlopen", side_effect=TimeoutError),
        ):
            with self.assertRaises(TimeoutError):
                generate(self.factor, self.docs)

    def test_valid_json_and_protocol(self):
        payload = {"claims": [{"text": "Contexto geral", "source_ids": ["E02"]}]}
        with (
            patch.dict(
                os.environ,
                {"OLLAMA_MODEL": "qwen2.5:3b", "OLLAMA_URL": "http://localhost:11434"},
            ),
            patch(
                "urllib.request.urlopen", return_value=self.response(payload)
            ) as call,
        ):
            self.assertEqual(generate(self.factor, self.docs), payload["claims"])
            req = call.call_args.args[0]
            data = json.loads(req.data)
            self.assertFalse(data["stream"])
            self.assertEqual(data["format"], "json")
            self.assertNotIn("inputs", json.loads(data["messages"][1]["content"]))

    def test_invalid_citation_and_json_rejected(self):
        with patch.dict(os.environ, {"OLLAMA_MODEL": "qwen2.5:3b"}):
            with patch(
                "urllib.request.urlopen",
                return_value=self.response(
                    {"claims": [{"text": "x", "source_ids": ["false"]}]}
                ),
            ):
                with self.assertRaises(ValueError):
                    generate(self.factor, self.docs)
            with patch("urllib.request.urlopen", return_value=io.BytesIO(b"not JSON")):
                with self.assertRaises(ValueError):
                    generate(self.factor, self.docs)

    def test_unconfigured_and_no_evidence(self):
        with patch.dict(os.environ, {"OLLAMA_MODEL": ""}):
            self.assertEqual(generate(self.factor, []), [])
            with self.assertRaises(RuntimeError):
                generate(self.factor, self.docs)
