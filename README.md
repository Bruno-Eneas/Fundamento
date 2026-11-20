# Fundamento | Avaliação laboratorial explicável

**Estado do produto: protótipo acadêmico demonstrativo, sem validação clínica, sem publicação pública comprovada.** Não integra sistemas da Unimed ou qualquer operadora. Não aceita dados de pacientes identificáveis como condição de uso da demonstração.

## Qual problema resolve

Apresenta resultados de exames de diabetes de forma explicável: qual valor foi usado, com qual faixa laboratorial foi comparado, por que o conjunto é inconclusivo ou requer confirmação e quais diretrizes fundamentam a interpretação. **Não emite diagnóstico, não exclui diabetes e não produz probabilidade clínica individual sem um modelo validado.**

## Executar no Windows

1. Extraia a pasta completa do ZIP em local de fácil acesso.
2. Instale Python 3.12. Na pasta Fundamento execute `Iniciar_Windows.bat` (cria `.venv`, instala dependências e abre Streamlit).
3. Abra a **Local URL** exibida no terminal. Não cole comandos dentro de `app.py`.
4. Na página **Exames**, clique nos exemplos A, B e C ou digite valores fictícios; clique em **Analisar exames**. Confira resultado, faixas e fontes.
5. Na aba **Análise**, explore a árvore de decisão histórica com dados fictícios e, opcionalmente, seus textos gerados por Ollama. Este escore **não** é a probabilidade da avaliação laboratorial.
6. Execute `Testar_Windows.bat` para a suíte completa. Confirme o resultado na sua máquina.

Opcional: com Ollama ativo, executar `ollama pull qwen2.5:3b` e abrir `Iniciar_Com_Ollama.bat` para geração **somente no módulo histórico**. O módulo Exames não requer Ollama.

## O que o módulo Exames recebe

- Glicemia plasmática em jejum (mg/dL), HbA1c (%) e, opcionalmente, TTGO 75 g de 1h/2h (mg/dL) ou glicemia plasmática casual (mg/dL).
- Informações declaradas sobre condições de coleta, gestação, faixa adulta, diagnóstico anterior, sintomas e possível interferência na HbA1c.
- PDF textual fictício anonimizado (até 5 MB, 8 páginas) com leitura **experimental** por rótulos. O operador deve conferir manualmente os números. PDFs escaneados ou ambíguos exigem digitação manual. **Não enviar documentos identificáveis.**

A avaliação é deliberadamente conservadora: resultados isolados na faixa de diabetes exigem confirmação em regra geral; resultados discordantes geram aviso; dados ausentes ou fora do escopo geram abstenção. Em qualquer caso a tela explica as fontes e a ausência de probabilidade individual validada.

## Fontes prioritárias

1. [SBD — Diagnóstico de diabetes mellitus, edição 2026](https://diretriz.diabetes.org.br/diagnostico-de-diabetes-mellitus/)
2. [ADA — Standards of Care in Diabetes, seção 2, 2026](https://doi.org/10.2337/dc26-s002)
3. [NIDDK/NIH — Diabetes Tests & Diagnosis](https://www.niddk.nih.gov/health-information/diabetes/overview/tests-diagnosis)

As faixas estão em `src/clinical.py`; links não representam aprovação da plataforma por essas organizações.

## Arquitetura

| Arquivo | Função |
|---|---|
| `app.py` | Interface, navegação, formulários, avisos e visual claro/escuro |
| `src/clinical.py` | Regras de faixa e abstenção, retorno estruturado e fontes |
| `src/lab_pdf.py` | Leitura local conservadora de PDFs textuais demonstrativos |
| `src/core.py` / `src/charts.py` | Modelo histórico e gráfico SHAP, **separados** |
| `src/generation.py` / `src/session.py` | Gerador Ollama opcional e controle transacional |
| `src/storage.py` | Banco de feedback do módulo histórico, SQLite ou PostgreSQL |
| `assets/theme.css`, `hero_*.svg` | Tema visual e paisagens próprias em verde |
| `tests/` | Suíte de regressões clínicas, leitura PDF e modelo histórico |
| `docs/Entrega/` | Relatório técnico, plano e apresentação **para conferência** |

## Requisitos do professor e entregas

O enunciado oficial em `docs/Enunciado.pdf` exige: aplicativo funcional publicamente acessível; relatório técnico **15–25 páginas** com 22 tópicos; plano de disseminação **5–10 páginas**; apresentação de **15 minutos** e arguição de **20 minutos**; declaração de uso de IA. A pasta `docs/Entrega/` traz versões acadêmicas preparadas para conferência. **Data/hora final, nomes dos colegas, URL pública, testes Windows e revisão médica ainda faltam.**

## Limites e privacidade

Esta aplicação não possui autenticação, adequação completa à LGPD, sistema de prontuário ou modelo de predição clínica calibrado. Evitar uso com exames de pessoas reais mesmo quando hospedada. As entradas não são deliberadamente salvas pelo módulo Exames, mas toda hospedagem tem riscos de infraestrutura/logs; não interpretar essa restrição de código como certificação de privacidade. Avaliar governança, segurança e regulação antes de qualquer piloto com pacientes.

## Treinamento e artefatos históricos

**Não execute `train.py` para testar o site**: baixa dados e pode sobrescrever o modelo antigo. O modelo `.joblib` deve ser carregado apenas deste pacote confiável. A árvore histórica usa idade codificada, IMC, atividade física e hipertensão; não recebe glicemia nem HbA1c. Suas métricas e dados de treinamento não validam a interpretação laboratorial.

## Git

A pasta `.git` e o `Fundamento.bundle` preservam o histórico real disponível. Não alterar datas/autoria para simular trabalho de integrantes. Consulte `docs/Git.md`.
