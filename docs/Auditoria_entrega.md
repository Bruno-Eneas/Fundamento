# Fundamento — auditoria para a entrega de SCOM
20/11/2026. Esta nota atualiza o estado descrito no PDF de continuidade. O enunciado, o horário final e os mockups aprovados continuam pendentes.

## Resultado técnico
O modelo distribuído, sem novo treinamento, reproduziu as saídas de 2,23%, 39,28% e 25,87% para A, B e C. A referência SHAP foi 13,4232% nos três. No B, as contribuições foram +11,6875, +10,6805, +3,4915 e 0,0000 pontos percentuais para hipertensão, IMC, idade e atividade. Zero corresponde ao comportamento desta árvore.

O CSV baixado da origem coincidiu com o SHA-256 de assets/metrics.json. Reconstituímos as partições por perfil e conferimos os três pares sem interseção. O limiar 0,13 maximizou a acurácia balanceada na grade de validação. No teste, reproduzimos a matriz [[22335,16451],[1390,5953]], ROC AUC 0,755376, AP 0,326404 e Brier 0,118781. Das 22404 previsões positivas, 5953 corresponderam à classe 1. Acurácia de 61,32%, sensibilidade de 81,07%, especificidade de 57,59%. O particionamento por perfil testa generalização interna a combinações ausentes do treino. A aplicação em outra população exige evidência própria.

## Problemas e aceite
| Prioridade | Local e constatação | Ação e verificação |
|---|---|---|
| Alta | app.py, formulário. Reproduzido em AppTest: uma seleção e comentário sobre B permaneciam na avaliação seguinte. | O formulário ganha identidade nova quando a explicação é recalculada ou há tentativa de geração. O teste em tests/test_app.py salva B e verifica A com a opção e o comentário vazios. |
| Média | app.py, Método. O destaque para AUC e AP deixava a precisão positiva dependente da leitura da matriz. | A tela agora mostra as três taxas e a contagem dos positivos. Conferir com a matriz do teste. |
| Baixa | app.py, barra lateral. A descrição de atividade omitia a exclusão de atividade no trabalho. | Legenda alinhada à tabela de variáveis da UCI. |
| Alta para alegações clínicas | train.py e assets/metrics.json. A classe 1 tem uma definição catalogada. O vínculo com a codificação original ainda requer documentação. | Citar o dicionário da UCI e distinguir ano do levantamento, ano bibliográfico e depósito. A página cita 2017, foi vinculada em 2023 e aponta ao BRFSS 2014. Conferir a transformação a partir dos dados originais e os termos da fonte antes de afirmar ano de coleta ou licença específica. |
| Média | src/core.py, retrieve e validate_generated. Três trechos distintos de uma página; há só um documento elegível por fator coberto. O identificador correto pode acompanhar uma frase sem apoio. | No ensaio, abrir cada trecho citado e comparar a frase gerada. Manter explícita a lacuna para hipertensão. A curadoria e a revisão por especialista são etapas distintas. |
| Pendente de observação | app.py e assets/theme.css. Chromium não iniciou o processo local por restrição de socket. | Conferir no navegador a barra superior, textos, seletores, rodapé, gráfico e tabela nos dois temas, em 1366 e 390 px, com os mockups do grupo. |
| Alta para entrega | Enunciado ausente. O PDF de continuidade descreve o protótipo. | Obter enunciado e prazo completo. Para cada exigência, indicar responsável, arquivo, evidência e status. Definir slides e relatório acadêmico conforme a rubrica. |

## Roteiro para o grupo
1. Extrair o ZIP numa pasta nova. Abrir Iniciar_Windows.bat com Python 3.12 instalado. Abrir a Local URL impressa no terminal. O script train.py sobrescreve os artefatos e é dispensável para a demonstração.
2. Abrir Testar_Windows.bat. Esperado: 16 testes, OK. No app, avaliar B, trocar para A e conferir que a opção e o comentário recomeçam vazios. Abrir o gráfico de A para barras negativas, B para positivas e a tabela para o zero.
3. Baixar o JSON em cada perfil. Comparar case, inputs, score e fatores com a tela; verificar retrieved.HighBP vazio. A seção Método deve mostrar precisão positiva de 26,57%.
4. Para geração, manter Ollama em execução e rodar no CMD: ollama pull qwen2.5:3b. Abrir Iniciar_Com_Ollama.bat e usar a URL dessa instância. Conferir rascunhos palavra por palavra. Após um sucesso, interromper somente o serviço de teste, tentar gerar de novo e conferir que generated_draft desapareceu do novo JSON.
5. SQLite foi exercitado localmente com banco temporário. Se hospedagem for exigida, validar em outra máquina a geração e a recuperação das avaliações após reinício, com a configuração final do banco.
6. Reunir enunciado, prazo e imagens de referência. Divisão sugerida: uma pessoa testa a instalação e registra evidências, outra confere dados e fontes, e a terceira confronta os materiais acadêmicos com a rubrica.

## Fontes consultadas
- UCI, CDC Diabetes Health Indicators. https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
- NIDDK, Risk Factors for Type 2 Diabetes. Os três trechos cadastrados correspondem à seção sobre fatores de risco. https://www.niddk.nih.gov/health-information/diabetes/overview/risk-factors-type-2-diabetes

## Alcance da execução
Suíte com Python 3.12 e dependências do projeto. AppTest exercita os widgets e o estado da aplicação. O teste do conector utiliza respostas HTTP simuladas. Windows real, Ollama ao vivo, PostgreSQL, publicação e inspeção visual em navegador seguem pendentes. O registro desta execução acompanha esta nota em Testes_auditoria.txt.
