"""Avaliação laboratorial educativa, com regras explícitas e opção de abstenção.

Não diagnostica nem estima probabilidade individual; exige revisão clínica.
Referências: SBD 2026, ADA 2026 e NIDDK (links em SOURCES).
"""
from dataclasses import dataclass, asdict
import math
from typing import Optional

SOURCES = {
    "SBD-2026": {"title": "Sociedade Brasileira de Diabetes — Diagnóstico de diabetes mellitus (2026)", "url": "https://diretriz.diabetes.org.br/diagnostico-de-diabetes-mellitus/"},
    "ADA-2026": {"title": "American Diabetes Association — Diagnosis and Classification, Standards of Care 2026", "url": "https://doi.org/10.2337/dc26-s002"},
    "NIDDK": {"title": "National Institute of Diabetes and Digestive and Kidney Diseases — Diabetes Tests & Diagnosis", "url": "https://www.niddk.nih.gov/health-information/diabetes/overview/tests-diagnosis"},
}

ANALYTES = {
    "glicemia_jejum": ("Glicemia plasmática em jejum", "mg/dL", 100, 126),
    "hba1c": ("Hemoglobina glicada (HbA1c)", "%", 5.7, 6.5),
    "ttgo_1h": ("TTGO 75 g, 1 hora", "mg/dL", 155, 209),
    "ttgo_2h": ("TTGO 75 g, 2 horas", "mg/dL", 140, 200),
}


@dataclass
class ClinicalResult:
    status: str
    headline: str
    explanation: str
    measurements: list[dict]
    notes: list[str]
    next_steps: list[str]
    source_ids: list[str]
    probability: Optional[float] = None
    probability_reason: str = (
        "Não estimada: o projeto não dispõe de modelo calibrado, avaliado externamente "
        "e validado para calcular probabilidade individual a partir destes exames."
    )
    research_only: bool = True

    def to_dict(self):
        return asdict(self)


def _num(name, value):
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        raise ValueError(f"Valor inválido para {name}.")
    try:
        v = float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        raise ValueError(f"Valor inválido para {name}.") from None
    if not math.isfinite(v):
        raise ValueError(f"Valor inválido para {name}.")
    bounds = (3.0, 25.0) if name == "hba1c" else (20.0, 1000.0)
    if not bounds[0] <= v <= bounds[1]:
        raise ValueError(f"{name}: valor fora do intervalo operacional. Confira unidade e digitação.")
    return v


def evaluate_labs(
    values: dict,
    *,
    adult: bool = True,
    pregnant: bool = False,
    known_diabetes: bool = False,
    fasting_confirmed: bool = True,
    ogtt_75g_confirmed: bool = True,
    certified_a1c: bool = True,
    a1c_interference: bool = False,
    classic_symptoms: bool = False,
) -> ClinicalResult:
    """Relaciona resultados laboratoriais a critérios públicos; nunca emite diagnóstico.

    A presença de resultados discordantes bloqueia afirmações conclusivas.
    Valores não interpretáveis são mencionados e excluídos da análise.
    """
    values = values or {}
    collected = {k: _num(k, values.get(k)) for k in (*ANALYTES, "glicemia_casual")}
    rows, notes, next_steps = [], [], []

    def outcome(status, headline, explanation, next_steps_override=None):
        return ClinicalResult(
            status=status, headline=headline, explanation=explanation,
            measurements=rows, notes=notes,
            next_steps=next_steps_override if next_steps_override is not None else next_steps,
            source_ids=["SBD-2026", "ADA-2026", "NIDDK"],
        )

    if known_diabetes:
        return outcome("fora_escopo", "Avaliação diagnóstica não aplicável",
                       "O perfil indica diagnóstico prévio. O acompanhamento é diferente de uma triagem inicial.",
                       ["Utilizar protocolo de acompanhamento com profissional de saúde."])
    if not adult or pregnant:
        return outcome("fora_escopo", "Avaliação automática não aplicável",
                       "Os critérios desta demonstração são voltados à avaliação inicial de adultos fora da gestação.",
                       ["Utilizar critérios específicos para gestação ou menores de 18 anos com profissional de saúde."])

    positive = []
    intermediate = []
    normal = []
    invalid = []
    for key, (label, unit, low, high) in ANALYTES.items():
        val = collected[key]
        if val is None:
            continue
        if key == "glicemia_jejum" and not fasting_confirmed:
            category = "não interpretável"
            invalid.append(key)
            notes.append("Glicemia informada sem confirmação de jejum adequado; não classificada como glicemia de jejum.")
        elif key.startswith("ttgo_") and not ogtt_75g_confirmed:
            category = "não interpretável"
            invalid.append(key)
            notes.append("TTGO sem confirmação da carga de 75 g; não utilizado.")
        elif key == "hba1c" and (not certified_a1c or a1c_interference):
            category = "não interpretável"
            invalid.append(key)
            notes.append("HbA1c com possível interferência ou método não confirmado; não utilizada na classificação.")
        else:
            category = "critério laboratorial na faixa de diabetes" if val >= high else ("faixa intermediária" if val >= low else "abaixo da faixa intermediária")
            if val >= high:
                positive.append(key)
            elif val >= low:
                intermediate.append(key)
            else:
                normal.append(key)
        rows.append({"exame": label, "valor": val, "unidade": unit, "interpretação": category, "referência": "SBD-2026"})

    casual = collected["glicemia_casual"]
    if casual is not None:
        if casual >= 200 and classic_symptoms:
            cat = "glicemia casual ≥200 com sintomas típicos relatados"
            positive.append("glicemia_casual_sintomas")
        else:
            cat = "informação complementar, sem critério conclusivo isolado"
            notes.append("Glicemia casual só fundamenta o critério específico quando ≥200 mg/dL e acompanhada de sintomas típicos.")
        rows.append({"exame": "Glicemia plasmática casual", "valor": casual,
                     "unidade": "mg/dL", "interpretação": cat, "referência": "SBD-2026"})

    if not rows:
        return outcome("dados_insuficientes", "Não há exames para analisar",
                       "Informe ao menos um exame laboratorial elegível. O sistema não pode concluir a partir de campos vazios.",
                       ["Informar glicemia plasmática de jejum e/ou HbA1c com unidade e condições de coleta."])

    if "glicemia_casual_sintomas" in positive:
        next_steps.append("Procurar avaliação médica prontamente, especialmente se houver mal-estar ou sintomas intensos.")
        return outcome("necessita_avaliacao", "Critério laboratorial associado a sintomas típicos",
                       "Uma glicemia casual ≥200 mg/dL com sintomas típicos atende ao critério laboratorial descrito pelas diretrizes. A informação relatada exige avaliação clínica; o aplicativo não determina o diagnóstico.")

    # Os tempos de 1h e 2h pertencem ao mesmo TTGO e não são contados
    # automaticamente como testes independentes para confirmação.
    independent = (
        ("hba1c" in positive and any(k in positive for k in
            ("glicemia_jejum", "ttgo_1h", "ttgo_2h")))
        or ("glicemia_jejum" in positive and any(k in positive for k in
            ("ttgo_1h", "ttgo_2h")))
    )
    if independent:
        next_steps.append("Levar os exames, datas de coleta e contexto clínico a um profissional de saúde para interpretação e confirmação adequada.")
        return outcome("criterios_concordantes", "Dois critérios laboratoriais na faixa de diabetes",
                       "Dois exames diferentes estão na faixa laboratorial descrita nas diretrizes. Em situações apropriadas, resultados concordantes podem atender à exigência de confirmação; cabe ao profissional verificar amostra, método e contexto clínico.")

    if positive:
        next_steps.append("Repetir ou complementar o teste alterado conforme avaliação médica e conferir fatores que interferem na HbA1c.")
        if normal or intermediate:
            return outcome("inconclusivo", "Exames discordantes: confirmação necessária",
                           "Há um critério na faixa de diabetes, mas os exames não são concordantes. Recomenda-se confirmar o resultado alterado e investigar interferências antes de concluir.")
        return outcome("confirmacao_pendente", "Resultado alterado: confirmação necessária",
                       "Um resultado isolado atingiu a faixa laboratorial de diabetes, mas geralmente é necessária confirmação por novo resultado, salvo exceções clínicas específicas.")

    if intermediate:
        next_steps.append("Discutir acompanhamento e eventual complementação dos exames com profissional de saúde.")
        return outcome("faixa_intermediaria", "Resultado na faixa intermediária (pré-diabetes)",
                       "Ao menos um exame está na faixa intermediária definida pelas diretrizes. Isso não significa que a pessoa inevitavelmente desenvolverá diabetes.")

    if not normal:
        return outcome("dados_insuficientes", "Sem exames elegíveis para conclusão",
                       "Os valores fornecidos não puderam ser usados com segurança nas condições informadas.",
                       ["Conferir condições de coleta e preencher exames laboratoriais interpretáveis."])
    next_steps.append("Se houver sintomas ou fatores de risco importantes, discutir necessidade de investigação adicional com profissional de saúde.")
    return outcome("sem_criterio_nos_dados", "Sem alteração nas faixas avaliadas",
                   "Os exames informados e interpretáveis ficaram abaixo das faixas intermediárias consideradas. Isso não exclui diabetes nem substitui avaliação clínica.")
