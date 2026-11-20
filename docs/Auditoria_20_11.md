# Fundamento | Auditoria independente de código, método e entrega

**Data:** 20/11/2026. **Fonte acadêmica:** `docs/Enunciado.pdf`.

## Escopo observado

Conferidos `app.py`, `assets/*`, `src/*.py`, `train.py`, `requirements.txt`, testes, documentação, scripts e histórico Git. O arquivo distribuído `assets/model.joblib` foi carregado localmente com scikit-learn 1.8.0, e os três perfis foram recalculados; o modelo **não foi retreinado**. Não executamos Ollama, Windows, PostgreSQL, publicação nem teste visual navegador. A suíte completa desta sessão **não pôde ser concluída** porque o ambiente dispõe de Python 3.13 sem Streamlit/Altair e a instalação de dependências não teve acesso à rede. Os testes executáveis sem essas bibliotecas passam. Os 16 testes originalmente reportados no pacote são registro anterior, e não resultado independente desta execução.

## Matriz de problemas

| Gravidade | Local / função | Evidência por leitura ou execução | Efeito | Ação indicada | Teste de aceite |
|---|---|---|---|---|---|
| **Crítica para entrega** | Documentos e publicação | Enunciado p. 4 exige URL pública; não há link publicado no pacote, `docs/Git.md` informa nenhum remoto | -10 pontos previstos e demonstração inacessível | Implantar Streamlit em ambiente Python e disponibilizar URL | Abrir URL em navegador anônimo de outra máquina, analisar A/B/C, conferir limitações e registrar captura |
| **Alta para entrega** | Documentação e slides | Enunciado p. 4–5 exige relatório 15–25p, plano 5–10p e pitch 15min + 20min; PDF é apenas continuidade | Entregas obrigatórias ausentes | Produzir os três materiais completos, com evidências | Recontar páginas e itens; ensaiar fala cronometrada |
| **Alta para inovação** | `src/core.py:retrieve`, `assets/evidence.json` | Apenas três resumos de **uma** página NIDDK/NIH, sem documento elegível para `HighBP` | Busca restrita, diferenciação e contexto brasileiro fracos | Ampliar corpus somente com fonte conferida; considerar diretrizes SBD 2026 | Conferir URL, trecho literal, data, fator e abstenção na ausência de suporte |
| **Alta para afirmações clínicas** | `train.py`, `assets/metrics.json`, `app.py` | Modelo só usa Age, BMI, PhysActivity e HighBP; sem HbA1c/glicemia; rótulo combina pré-diabetes e diabetes | Confusão entre saída algorítmica e diagnóstico/prognóstico | Evidenciar classe histórica e limitações na tela, relatório e apresentação | Médica/o voluntário compreende o fluxo sem interpretar número como risco individual validado |
| **Alta de qualidade** | `src/core.py:validate_generated` | IDs são validados, mas suporte semântico da frase não é; sem revisão humana automática | Rascunho com fonte real pode conter afirmação sem apoio | Preservar aviso de rascunho e exigir comparação humana de cada frase; bloquear saídas excessivas | Resposta com ID falso, texto vazio, repetição e mais de 6 afirmações deve ser barrada |
| **Média** | `app.py` página Análise | Classificação mostrava `Classe 1/0` com legenda pouco explícita; a referência era apresentada como proporção do treino | Usuário leigo pode confundir as duas grandezas | Legenda explicada e rótulos das métricas mais claros **corrigidos** | Abrir B e pedir que terceiro explique classe 1, escore e referência |
| **Média** | `src/storage.py:save_feedback` | Avaliações com SQLite local ou PostgreSQL configurável, sem autenticação/limitação de envios | Plataforma pública vulnerável a spam e perda de avaliações em armazenamento efêmero | Definir política de coleta/retenção, limites de envio e banco durável se persistência for necessária | Enviar avaliação, reiniciar host e conferir banco; tentar envios repetidos em homologação |
| **Média** | `app.py`, `assets/theme.css` | CSS customizado com seletores internos do Streamlit, captura aprovada não fornecida | Visual pode variar por versão/viewport, contraste não comprovado | Testar em 1366 px e 390 px nos dois temas, com mockups | Capturas de todos os estados, rolagem, gráfico e rodapé sem corte |
| **Média** | `src/generation.py:generate` | Chamadas por fator com timeout 90s; testes HTTP simulados | Lento/offline, não demonstra confiabilidade em hospedagem | Testar serviço real, feedback e indisponibilidade sem exportar rascunhos antigos | Gerar, interromper serviço, repetir, baixar JSON sem rascunho anterior |
| **Média** | `train.py:main` | Download CSV e **sobrescrita** de `assets/model.joblib` e `metrics.json` | Executar inadvertidamente destrói a versão de referência | Não executar como teste; backup antes de re-treino; idealmente exigir sinalizador de sobrescrita | Comparar hash do artefato antes/depois do teste sem rodar `train.py` |
| **Baixa de embalagem** | `README.md`, `docs/Git.md`, `COMECAR_AQUI.txt` | Pacote original mencionava bundle e HISTORICO_COMMITS, mas estes não constavam no ZIP inspecionado | Instruções de restauração incompletas | Gerar `Fundamento.bundle` e `HISTORICO_COMMITS.txt` atuais **corrigidos nesta entrega** | `git bundle verify Fundamento.bundle` e `git log --oneline` |
| **Pendente** | `docs/Uso_de_IA.md` e relatório | Há registro preliminar, mas não relatório com finalidade, trechos gerados, mudanças e avaliação crítica | Penalidade acadêmica potencial | Completar seção 18 com auditoria do uso de IA | Conferir cinco itens da p. 7 do enunciado |

## Método confirmado e limites

- **Execução local:** Caso A 2,2287375%; B 39,2826497%; C 25,8692788%. Referência SHAP 13,4231790%. B: HighBP +11,6875 p.p., BMI +10,6805, Age +3,4915 e PhysActivity 0. As somas são verificadas em `src/core.explain`.
- **Conferência aritmética do JSON:** matriz `[ [22335,16451], [1390,5953] ]`; precisão positiva = 5.953/22.404 = 26,57%; sensibilidade 81,07%; especificidade 57,59%; acurácia 61,32%. ROC AUC 0,7554, AP 0,3264, Brier 0,1188 são valores **registrados**, não recalculados do CSV nesta execução.
- **Fonte UCI consultada:** `Diabetes_binary`: 0 = no diabetes, 1 = prediabetes or diabetes. Aponta BRFSS 2014; registro UCI vinculado em 25/09/2023 e referência bibliográfica da página em 2017. Licença remete ao conjunto vinculado e exige conferência antes de republicação.
- **Fonte NIDDK consultada:** os três excertos cadastrados sobre idade, excesso de peso e inatividade física constam na página Risk Factors for Type 2 Diabetes. Contexto é diabetes tipo 2; não valida rótulo combinado nem previsão do modelo.
- **Fonte brasileira para evolução (não integrada ao RAG):** https://diretriz.diabetes.org.br/ (Diretriz SBD 2026). Os critérios de diagnóstico requerem exames que não entram no modelo atual. Incluir apenas após curadoria, autoria e revisão.

## Corrigido neste pacote

1. `app.py`: legenda detalha o que significa o alvo binário e distingue proporção do grupo e referência histórica.
2. `src/core.py:validate_generated`: máximo de seis afirmações e até três IDs distintos por afirmação. Ainda não há verificação semântica de suporte.
3. `tests/test_core.py`: regressões para quantidade excessiva e IDs duplicados.
4. `docs/Enunciado.pdf`, `docs/Matriz_requisitos.md` e esta auditoria; bundle e histórico Git incluídos no pacote atualizado.

## Aceite no Windows (sem inventar resultado)

1. Extrair pasta toda, instalar Python **3.12** e abrir `Iniciar_Windows.bat`.
2. No terminal da pasta, executar `Testar_Windows.bat`. **Esperado após esta revisão: 17 testes OK**, mas o resultado deve ser registrado localmente. Não use `train.py` para testar.
3. Em **Análise**, conferir Caso B e abrir todos os fatores (inclusive `HighBP` sem documento elegível), gráfico de contribuições e tabela. Mudar para A e C, conferir valores e classificações; baixar JSON de cada caso.
4. Testar navegação Evidências/Método, tema claro/escuro e janela estreita. Conferir cabeçalho, legibilidade, botões, contraste e fim da página; salvar prints reais.
5. Para geração, instalar Ollama e `ollama pull qwen2.5:3b`, abrir `Iniciar_Com_Ollama.bat`, gerar e confrontar cada texto com o trecho citado. Simular serviço desligado e verificar ausência de rascunho antigo no JSON.
6. Salvar avaliação fictícia, reiniciar aplicativo, confirmar persistência. Em hospedagem com banco remoto, testar de outra máquina.
7. Publicar e obter URL. Incluir no relatório, anexar captura da URL funcionando; finalizar e validar relatório 15–25p, plano 5–10p, pitch 15min, arguição 20min e seção obrigatória de IA.

## Fontes verificadas externamente em 20/11/2026

- Enunciado do professor, `docs/Enunciado.pdf`, p. 1–7.
- https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
- https://www.niddk.nih.gov/health-information/diabetes/overview/risk-factors-type-2-diabetes
- https://diretriz.diabetes.org.br/
- https://docs.streamlit.io/deploy/streamlit-community-cloud

A auditoria não equivale a validação clínica, aceite do professor nem publicação real.
