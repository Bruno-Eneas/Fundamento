# Fundamento — protótipo acadêmico

**Objetivo demonstrável:** organizar exames fictícios por paciente e data, exibir um resultado laboratorial compreensível ao paciente e permitir ao médico consultar a justificativa, as fontes e o histórico, além de registrar notas de acompanhamento.

> **Não é sistema clínico.** Não confirma o tipo 2, não calcula probabilidade individual validada, não deve receber dados de pessoas reais. Nenhum vínculo institucional com Unimed, SBD ou ADA está alegado.

## O caminho mais fácil para apresentar

1. Instale **Python 3.12** no Windows, se necessário.
2. Extraia o ZIP inteiro e execute **`APRESENTAR_WINDOWS.bat`**. O iniciador cria um ambiente isolado e instala as bibliotecas na primeira execução.
3. Abra a **Local URL** que o terminal mostrar.
4. Clique em **Entrar como médico (demo)**. Selecione **DEMO-001** e confira a conclusão, a evolução e a justificativa; pode registrar um exame *fictício* ou uma observação.
5. Clique em **Sair da conta** e depois **Ver área do paciente (demo)**: somente um cartão de resultado e as datas, sem gráficos ou SHAP.

O modo de apresentação não exige senha **porque não possui autenticação**. Ele é ativado explicitamente e o iniciador restringe o servidor ao próprio computador (`127.0.0.1`). Não o utilize com dados reais.

## Uso normal local com senhas demonstrativas

Execute **`Iniciar_Windows.bat`**. O sistema criará contas e senhas aleatórias em `runtime/ACESSOS_DEMONSTRACAO.txt` na primeira execução. O acesso simula separação por perfis, **não é autorização ou prontuário seguro**. Teste com `Testar_Windows.bat`.

## Vitrine pública acadêmica — somente leitura

É possível publicar um demonstrador Streamlit com `FUNDAMENTO_PUBLIC_SHOWCASE=1` nas variáveis de ambiente do servidor. Esse modo libera dois botões de visita com **dados fictícios**, sem formulários de escrita ou autenticação. A hospedagem **não garante persistência do SQLite local**; a vitrine reinicia os perfis predefinidos quando necessário. Esse recurso não é equivalente a publicar um prontuário com controle de acesso. Veja `docs/ENTREGA_SIMPLES.md`.

## Estrutura

- `app.py`: navegação, temas e formulários.
- `src/patients.py`: perfis fictícios, exames e notas em SQLite local.
- `src/portal.py`: tela simples do paciente e área detalhada do médico.
- `src/clinical.py`: critérios laboratoriais explícitos, confirmações e abstenção.
- `src/auth.py`: senhas aleatórias para o fluxo local tradicional.
- `src/showcase.py`: modos de apresentação sem login (intencionalmente sem autenticação).
- `src/lab_pdf.py`: extração experimental somente de PDF textual fictício, sujeita à conferência.
- `src/core.py`, `src/charts.py`, `src/generation.py`, `src/session.py`: modelo e geração **experimentais**, independentes da análise de exames; Ollama opcional.
- `assets/`: modelo demonstrativo, regras, referências e temas verdes com pinheiros.
- `tests/`: testes automatizados.
- `docs/Entrega/`: arquivos editáveis e PDFs do relatório e plano, apresentações e roteiro; devem permanecer coerentes com a versão efetivamente publicada.

## O que deliberadamente não prometemos

- Diagnóstico automático definitivo; identificação do tipo 2 por exames de rotina; previsão do aparecimento futuro da doença; porcentagem clínica individual.
- Chat médico com RAG integrado ao histórico: **não implementado**. As fontes clínicas são cadastradas e mostradas diretamente; o gerador antigo é separado e opcional.
- Importação segura de exames de pacientes reais; compatibilidade com prontuários; assinatura ou acesso médico institucional; conformidade completa com LGPD.

**Fontes de critérios:** [Sociedade Brasileira de Diabetes — Diagnóstico 2026](https://diretriz.diabetes.org.br/diagnostico-de-diabetes-mellitus/), [ADA — Standards 2026](https://doi.org/10.2337/dc26-s002) e [NIDDK/NIH](https://www.niddk.nih.gov/health-information/diabetes/overview/tests-diagnosis). A revisão clínica independente permanece necessária.

**Entrega:** ler `docs/ENTREGA_SIMPLES.md` e o `docs/Enunciado.pdf`. A URL pública e os testes no Windows não podem ser considerados comprovados antes de executados pelo grupo.
