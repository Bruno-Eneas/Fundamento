"""Treinamento reproduzível; baixar dados sem redistribuir o CSV no pacote."""

import hashlib, json, sys, urllib.request
from pathlib import Path
import joblib, numpy as np, pandas as pd, sklearn, shap
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    classification_report,
    balanced_accuracy_score,
)
from src.core import FEATURES

ROOT = Path(__file__).parent


def main(path=None):
    if path is None:
        path = ROOT / "runtime/data.csv"
        path.parent.mkdir(exist_ok=True)
        urllib.request.urlretrieve(
            "https://archive.ics.uci.edu/static/public/891/data.csv", path
        )
    df = pd.read_csv(path)
    assert set(df.Diabetes_binary.unique()) == {0, 1}
    assert not df[FEATURES + ["Diabetes_binary"]].isna().any().any()
    X = df[FEATURES]
    y = df.Diabetes_binary
    # Perfis idênticos nas quatro entradas ficam em apenas um lado da divisão.
    groups = pd.util.hash_pandas_object(X, index=False)
    train, test = next(
        GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42).split(
            X, y, groups
        )
    )
    inner_train, inner_val = next(
        GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=43).split(
            X.iloc[train], y.iloc[train], groups.iloc[train]
        )
    )
    val = train[inner_val]
    train = train[inner_train]
    model = DecisionTreeClassifier(max_depth=4, min_samples_leaf=500, random_state=42)
    model.fit(X.iloc[train], y.iloc[train])
    val_score = model.predict_proba(X.iloc[val])[:, 1]
    thresholds = np.linspace(0.05, 0.5, 46)
    threshold = float(
        max(
            thresholds,
            key=lambda t: balanced_accuracy_score(y.iloc[val], val_score >= t),
        )
    )
    score = model.predict_proba(X.iloc[test])[:, 1]
    pred = (score >= threshold).astype(int)
    metrics = {
        "rows": len(df),
        "train_rows": len(train),
        "validation_rows": len(val),
        "test_rows": len(test),
        "missing_values": int(df.isna().sum().sum()),
        "features": FEATURES,
        "seed": 42,
        "split": "GroupShuffleSplit: perfis idênticos agrupados; teste não usado para ajustar hiperparâmetros",
        "group_overlap": len(set(groups.iloc[train]) & set(groups.iloc[test])),
        "target": "Classe 1 de Diabetes_binary. UCI descreve como pré-diabetes ou diabetes; não diferencia tipo nem horizonte futuro. Conferência da codificação na fonte original pendente.",
        "source_url": "https://archive.ics.uci.edu/static/public/891/data.csv",
        "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        "class_counts": {str(k): int(v) for k, v in y.value_counts().items()},
        "roc_auc": roc_auc_score(y.iloc[test], score),
        "average_precision": average_precision_score(y.iloc[test], score),
        "brier": brier_score_loss(y.iloc[test], score),
        "positive_fraction_test": float(y.iloc[test].mean()),
        "threshold": threshold,
        "threshold_method": "Maior acurácia balanceada na validação; não é limiar médico",
        "confusion_matrix": confusion_matrix(y.iloc[test], pred).tolist(),
        "classification_report": classification_report(
            y.iloc[test], pred, output_dict=True, zero_division=0
        ),
        "versions": {"sklearn": sklearn.__version__, "shap": shap.__version__},
        "limitations": [
            "Amostra histórica dos EUA; não validada para a Unimed.",
            "Quatro variáveis: redução intencional para demonstração.",
            "Sem calibração clínica nem ajuste pelo plano amostral da pesquisa.",
            "Avaliação interna única; sem validação temporal ou externa.",
            "SHAP descreve o modelo e não causalidade.",
        ],
    }
    joblib.dump(model, ROOT / "assets/model.joblib")
    (ROOT / "assets/metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                k: metrics[k]
                for k in [
                    "rows",
                    "train_rows",
                    "test_rows",
                    "roc_auc",
                    "average_precision",
                    "confusion_matrix",
                    "group_overlap",
                ]
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
