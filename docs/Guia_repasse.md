# Fundamento 6 — guia para repassar ao integrante

## O que já está no pacote

O ZIP contém o aplicativo Streamlit, o tema verde claro/escuro com montanhas e pinheiros, o módulo de exames e critérios laboratoriais, importação experimental de PDF textual, resumos com motivos e sugestões de informação complementar, o antigo modelo de árvore + SHAP em seção separada, testes, documentação, apresentação editável e histórico Git.

**O que mudou nesta versão:** o resultado dos exames agora prioriza um cartão resumido, mostra as medidas mais importantes e informa apenas exames complementares condicionais. Essas alterações foram verificadas por testes de unidade, mas ainda exigem inspeção no Streamlit real.

## O que ainda falta fazer (ordem de prioridade)

1. **Testar no Windows**, validar todos os fluxos, visual de claro/escuro, exemplos e PDF; guardar as capturas reais. O ambiente de montagem não tinha Streamlit/Altair.
2. **Cadastrar pacientes fictícios** com identificadores e permitir criar, selecionar, editar e excluir perfis de demonstração, sem dados pessoais reais.
3. **Construir histórico longitudinal**: cada exame com data, unidade, origem e condições, associado ao perfil fictício; gráfico de evolução e comparação entre exames.
4. **Conectar RAG e chat ao histórico** com trechos de fontes confiáveis, referências verificáveis, revisão humana e resposta 'não sei' quando falta evidência. Ollama está só no módulo experimental, ainda não é chat do paciente.
5. **Conferir limites médicos e não inventar probabilidade** de diabetes tipo 2: o protótipo interpreta faixas laboratoriais, sem diagnóstico autônomo e sem modelo probabilístico clínico validado.
6. **Publicar site demonstrativo** em plataforma que rode Python/Streamlit, testar URL externa e persistência (sem permitir envio de exames reais).
7. **Revisar as entregas oficiais**: relatório 15–25 páginas, plano 5–10 páginas, pitch 15 minutos/arguição 20, declaração de IA, screenshots reais, integrantes, referências e URL pública.

## Rodar no Windows

- Extrair o ZIP completo para uma pasta nova.
- Instalar Python 3.12 e abrir `Iniciar_Windows.bat` na raiz da pasta `Fundamento`.
- Usar o endereço local mostrado no terminal, normalmente `http://localhost:8501` (confirmar número da porta).
- Abrir Exames laboratoriais, preencher os casos fictícios e clicar em Analisar exames.
- Rodar `Testar_Windows.bat`; documentar os testes que passaram e os que falharam.
- Para gerador opcional: instalar Ollama, executar `ollama pull qwen2.5:3b` e usar `Iniciar_Com_Ollama.bat`. O modo Exames não depende disso.
- **Não executar `train.py` para testar.**

## Casos mínimos para demonstrar

- Sem exames: insuficiente; sugere informações iniciais.
- Glicemia de jejum = 132 mg/dL: confirmação pendente; recomenda discutir HbA1c ou repetição.
- Glicemia = 132 e HbA1c = 6,8%: critérios laboratoriais concordantes; não rotular automaticamente tipo 2; probabilidade indisponível.
- Glicemia = 132 e HbA1c = 5,5%: discordantes; conferir exame alterado.
- Glicemia = 90 e HbA1c = 5,3%: abaixo das faixas intermediárias avaliadas; isso não exclui doença.
- Gestação, jejum não confirmado, possível interferência na HbA1c e PDF textual ambíguo devem ser verificados.

## Material de referência dentro do ZIP

- `docs/Enunciado.pdf`: regras oficiais do professor.
- `docs/Entrega/`: relatório, plano e slides a conferir.
- `docs/Prompt_continuidade.txt`: **não usar sem atualizar**, pois corresponde a escopo antigo. Prefira `docs/Prompt_terminar_projeto.txt`.
- `docs/Entrega/Pendencias_para_entrega.md`: pendências anteriores ao pacote 6.
- `src/clinical.py`: lógica da avaliação e sugestões; `app.py`: interface; `assets/theme.css`: layout; `tests/test_clinical.py`: regressão.
- `.git` + `Fundamento.bundle`: história de commits existente; não fabricar histórico.

## Confirmações que o grupo ainda precisa fornecer

Nomes/instituição e responsabilidades dos integrantes, data/hora exata da entrega (o enunciado não define a data), URL de publicação e validação por profissional habilitado, se houver.

**Atenção:** prévias em vídeo e imagens conceituais não são prova de operação real; não afirmar que o produto tem prontuário de pacientes, modelo de probabilidade clínica ou parceria institucional antes de implementar/comprovar.
