"""Estado transacional dos rascunhos: falhas nunca exportam texto anterior."""


def clear_generation(state):
    for key in ("generated", "generation_error"):
        state.pop(key, None)
    result = state.get("result")
    if result is not None:
        result.pop("generated_draft", None)


def generate_result(state, generator):
    clear_generation(state)
    result = state["result"]
    drafts = {}
    try:
        for factor in result["factors"]:
            docs = result["retrieved"][factor["feature"]]
            if docs:
                drafts[factor["feature"]] = generator(factor, docs)
    except Exception:
        clear_generation(state)
        state["generation_error"] = (
            "Geração indisponível ou resposta inválida. Nenhum texto gerado foi "
            "liberado; a consulta documental continua disponível."
        )
        return False
    state["generated"] = drafts
    result["generated_draft"] = drafts
    return True
