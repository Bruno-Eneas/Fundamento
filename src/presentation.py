"""Resumo de interface. NÃO classifica o tipo de diabetes nem calcula risco."""

SUMMARY = {
    "criterios_concordantes": (
        "ALERTA", "Exames na faixa laboratorial de diabetes",
        "Os resultados enviados precisam de avaliação médica. Eles não identificam, sozinhos, o tipo de diabetes.",
        "Converse com seu médico para revisar os exames."),
    "confirmacao_pendente": (
        "ALERTA", "Um exame apresentou alteração importante",
        "Há um resultado que pode precisar de confirmação.",
        "Converse com seu médico sobre a confirmação."),
    "inconclusivo": (
        "ATENÇÃO", "Os exames precisam ser esclarecidos",
        "Os resultados enviados não são concordantes.",
        "Peça ao seu médico para avaliar os exames."),
    "faixa_intermediaria": (
        "ACOMPANHAR", "Alguns resultados merecem atenção",
        "Um ou mais valores estão em uma faixa intermediária.",
        "Converse com seu médico sobre o acompanhamento."),
    "sem_criterio_nos_dados": (
        "SEM ALERTA NESTES EXAMES", "Não foram identificadas alterações nas faixas avaliadas",
        "Isso não garante ausência de diabetes nem substitui uma consulta.",
        "Mantenha o acompanhamento recomendado pelo seu médico."),
    "dados_insuficientes": (
        "SEM DADOS", "Faltam informações para avaliar",
        "Ainda não há informações suficientes para analisar os resultados.",
        "Solicite orientação médica para completar a avaliação."),
    "fora_escopo": (
        "AVALIAÇÃO MÉDICA", "Este caso precisa de avaliação individual",
        "A situação não pode ser interpretada automaticamente por este protótipo.",
        "Procure o médico responsável."),
    "necessita_avaliacao": (
        "ALERTA", "Resultados que exigem avaliação médica",
        "Os dados informados precisam de revisão médica.",
        "Procure avaliação médica."),
}


def brief_status(result):
    """Saída estável e enxuta para o paciente e o topo da área médica."""
    level, title, reason, next_step = SUMMARY.get(result.status, SUMMARY["dados_insuficientes"])
    return {"level": level, "title": title, "reason": reason, "next_step": next_step}
