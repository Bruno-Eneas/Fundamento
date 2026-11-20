# Plano de validação — módulo Exames

## O que está implementado

Comparação transparente de resultados laboratoriais com pontos de corte da SBD (edição 2026), padrões de confirmação da ADA (2026) e notas NIDDK. Interpretação determinística, recusando probabilidade individual não validada. Recebe apenas valores fictícios ou anonimizados e leitura experimental de PDF textual. Não há diagnóstico automatizado.

## Roteiro de verificação por casos fictícios

| Caso | Entrada | Resultado esperado |
|---|---|---|
| A | GJ 90 mg/dL; HbA1c 5,3% | Sem alteração nas faixas avaliadas; não exclui doença |
| B | GJ 132 mg/dL; HbA1c 6,8% | Dois critérios na faixa de diabetes; revisão profissional |
| C | GJ 94 mg/dL; HbA1c 6,7% | Discordância; confirmar alterado |
| D | GJ 110 mg/dL | Faixa intermediária (pré-diabetes) |
| E | GJ 135 mg/dL | Confirmação pendente |
| F | Nenhum exame | Dados insuficientes; não concluir |
| G | HbA1c 7,0% com interferência declarada | Não interpretável; abster-se se sem exames adicionais |
| H | Gestação ou menoridade | Fora do escopo |
| I | Glicemia casual 210 mg/dL, sem sintomas | Insuficiente para critério específico; orientar avaliação |
| J | Glicemia casual 210 mg/dL, com sintomas típicos | Critério sintomático; avaliação médica prontamente |

## Critérios para evolução a modelo probabilístico

1. Definir desfecho: presença de diabetes **atual** versus incidência **futura** em período específico. Não misturar os dois.
2. Selecionar base identificada, representativa e com glicemia/HbA1c efetivos, cronologia e padrão de referência para o rótulo.
3. Verificar licença, consentimento/uso secundário, viés de seleção e possíveis vazamentos de informação.
4. Partições independentes e, quando possível, validação externa/temporal; evitar pacientes duplicados.
5. Medir calibração (curva, Brier, erro de calibração), sensibilidade, especificidade, precisão, intervalos de confiança e desempenho por subgrupos permitidos.
6. Definir mecanismo formal de abstenção (ausência de dados, fora da distribuição, discordância e baixa confiança).
7. Submeter interpretação, riscos e linguagem a revisão clínica documentada, avaliação de usabilidade, privacidade e requisitos regulatórios.
8. **Somente então** habilitar porcentagem individual na interface, com definição explícita da população e do horizonte.

## Pontos ainda não executados

- Executar a suíte completa em Python 3.12 no Windows do grupo e anexar registro autêntico.
- Avaliar visualmente o Streamlit em Chrome/Edge nos dois temas e em tela estreita.
- Revisar critérios e textos com profissional de saúde; nenhuma validação ocorreu até agora.
- Publicar de forma pública (sem documentos de pacientes) e testar em dispositivo externo.
- Implementar autenticação, governança e requisitos de privacidade antes de qualquer projeto com exames reais.

## Fontes

SBD: https://diretriz.diabetes.org.br/diagnostico-de-diabetes-mellitus/

ADA: https://doi.org/10.2337/dc26-s002

NIDDK: https://www.niddk.nih.gov/health-information/diabetes/overview/tests-diagnosis
