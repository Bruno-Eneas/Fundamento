"""Modelo e evidências do protótipo. Nenhuma decisão diagnóstica é emitida."""

import json, math
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["Age", "BMI", "PhysActivity", "HighBP"]
LABELS = {
    "Age": "Faixa etária",
    "BMI": "IMC",
    "PhysActivity": "Atividade física",
    "HighBP": "Hipertensão relatada",
}
QUERIES = {
    "Age": "idade faixa etária diabetes",
    "BMI": "IMC excesso peso diabetes",
    "PhysActivity": "atividade física diabetes",
    "HighBP": "hipertensão pressão arterial diabetes",
}
AGES = [
    "18–24",
    "25–29",
    "30–34",
    "35–39",
    "40–44",
    "45–49",
    "50–54",
    "55–59",
    "60–64",
    "65–69",
    "70–74",
    "75–79",
    "80 ou mais",
]
CASES = {
    "Caso A — fictício": {"Age": 3, "BMI": 23, "PhysActivity": 1, "HighBP": 0},
    "Caso B — fictício": {"Age": 9, "BMI": 34, "PhysActivity": 0, "HighBP": 1},
    "Caso C — fictício": {"Age": 7, "BMI": 29, "PhysActivity": 1, "HighBP": 1},
}


def validate(values):
    for f in FEATURES:
        v = values.get(f)
        if (
            v is None
            or isinstance(v, bool)
            or not isinstance(v, (int, float))
            or not math.isfinite(v)
        ):
            raise ValueError(f"Informação ausente ou inválida: {LABELS[f]}.")
    if values["Age"] != int(values["Age"]) or not 1 <= values["Age"] <= 13:
        raise ValueError("Faixa etária fora das categorias da base.")
    if not 12 <= values["BMI"] <= 60:
        raise ValueError(
            "IMC fora do intervalo aceito para esta demonstração (12 a 60). Isso não é um limite clínico."
        )
    if any(values[f] not in (0, 1) for f in ["PhysActivity", "HighBP"]):
        raise ValueError("Campos binários devem ser 0 ou 1.")


def load_model():
    # Carregar somente o artefato confiável distribuído com este projeto.
    return joblib.load(ROOT / "assets/model.joblib")


def explain(values):
    validate(values)
    model = load_model()
    frame = pd.DataFrame([values], columns=FEATURES)
    explainer = shap.TreeExplainer(model, feature_perturbation="tree_path_dependent")
    explanation = explainer(frame)
    idx = list(model.classes_).index(1)
    score = float(model.predict_proba(frame)[0, idx])
    contributions = explanation.values[0, :, idx]
    base = float(explanation.base_values[0, idx])
    if not np.isclose(base + contributions.sum(), score, atol=1e-7):
        raise RuntimeError("A explicação não reconstruiu a saída. Resultado bloqueado.")
    rows = [
        {"feature": f, "label": LABELS[f], "value": values[f], "contribution": float(c)}
        for f, c in zip(FEATURES, contributions)
    ]
    return {
        "score": score,
        "base": base,
        "factors": sorted(rows, key=lambda x: abs(x["contribution"]), reverse=True),
        "model_version": "0.1",
        "knowledge_version": "0.1",
    }


def evidence():
    return json.loads((ROOT / "assets/evidence.json").read_text(encoding="utf-8"))


def retrieve(feature, threshold=0.05):
    # Filtro explícito evita usar evidência sobre idade para fundamentar pressão.
    docs = [d for d in evidence() if feature in d["features"] and d["active"]]
    if not docs:
        return []
    vec = TfidfVectorizer(strip_accents="unicode", ngram_range=(1, 2))
    matrix = vec.fit_transform([d["summary"] for d in docs])
    scores = (
        (matrix @ vec.transform([QUERIES.get(feature, feature)]).T).toarray().ravel()
    )
    return [
        {**d, "retrieval_score": float(score)}
        for d, score in sorted(zip(docs, scores), key=lambda t: t[1], reverse=True)
        if score >= threshold
    ][:2]


def rules():
    return json.loads((ROOT / "assets/rules.json").read_text(encoding="utf-8"))


def validate_generated(payload, retrieved):
    if not isinstance(payload, dict) or not isinstance(payload.get("claims"), list):
        raise ValueError("Resposta sem estrutura válida.")
    if len(payload["claims"]) > 6:
        raise ValueError("Número excessivo de afirmações geradas.")
    allowed = {x["id"]: x for x in retrieved}
    result = []
    for claim in payload["claims"]:
        if not isinstance(claim, dict):
            raise ValueError("Afirmação inválida.")
        ids = claim.get("source_ids", [])
        text = claim.get("text", "")
        if not isinstance(text, str) or not text.strip() or len(text) > 700:
            raise ValueError("Texto inválido.")
        if (
            not isinstance(ids, list)
            or not ids
            or len(ids) > 3
            or len(ids) != len(set(map(str, ids)))
            or any(not isinstance(i, str) or i not in allowed for i in ids)
        ):
            raise ValueError(
                "Citação não pertence aos documentos recuperados. Resposta bloqueada."
            )
        result.append({"text": text.strip(), "source_ids": ids})
    return result
