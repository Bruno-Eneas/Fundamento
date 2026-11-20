> **Nota posterior:** este relatório documenta o estado anterior ao recebimento do enunciado. Para requisitos oficiais, consulte `Enunciado.pdf` e `Matriz_requisitos.md`.

# Fundamento | Continuidade

## Entrega de 20 de novembro de 2026
Projeto demonstrativo de Daniel e dois colegas. Pacote de código revisado, testes, histórico Git e instruções para continuar em outra conversa. Este relatório substitui a versão de quatro páginas de 16/11. Não é o relatório acadêmico final exigido pelo professor.

## Objetivo e contexto
Explicar a saída de um modelo e permitir conferir fontes sobre indicadores de diabetes. O professor mencionou parceria com Unimed e possível IC. O aplicativo não tem vínculo institucional oficial, dados de pacientes reais ou validação clínica. Os três perfis são fictícios.

## Estado atual
A interface inicia com Caso B calculado; trocar caso recalcula. Temas claro branco/esmeralda e escuro petróleo, pinheiro, navegação Análise/Evidências/Método, fontes, gráfico SHAP, rascunho com Ollama, formulário de avaliação e download JSON. Modelo e fontes são os artefatos distribuídos anteriormente; não houve novo treinamento.

## Mudanças principais
Corrigida retenção de rascunho anterior após falha de geração; geração parcial não é liberada. A avaliação passou a exigir escolha explícita. CSS e gráfico foram separados em arquivos próprios, comentários e payloads inválidos são rejeitados. Testes ampliados, iniciadores adicionados e código Python formatado.

## O que continua aberto
Enunciado original, prazo completo e imagens aprovadas não estão no pacote. O usuário informou dia 22, mas os demais detalhes precisam de confirmação. Não declarar conformidade total, publicação, revisão médica ou fidelidade visual exata sem evidências. A entrega inclui código completo do protótipo; requisitos acadêmicos externos ainda dependem de confirmação.

# Arquitetura e dados

## Mapa do código
app.py: interface e exportação. assets/theme.css: visual. src/core.py: validação, SHAP e recuperação. src/charts.py: especificação do gráfico. src/session.py: estado de geração. src/generation.py: Ollama. src/storage.py: avaliações. train.py: treinamento opcional. tests/: suíte. docs/: documentação.

## Modelo e entradas
Árvore com profundidade máxima 4 e mínimo de 500 amostras por folha, seed 42. Usa Age (categoria 1–13, não idade literal), BMI, PhysActivity e HighBP. Não recebe glicemia, HbA1c ou histórico familiar. Intervalo de IMC 12–60 é restrição demonstrativa, não limite clínico.

## Base e divisão
Artefato proveniente da base histórica CDC/UCI, 253.680 registros. Treino 171.405, validação 36.146 e teste 46.129, separando grupos de perfis idênticos nas quatro entradas. Classes globais: 218.334 na classe 0 e 35.346 na classe 1. CSV não integra o pacote; hash e origem estão em assets/metrics.json.

## Desempenho registrado
ROC AUC 0,7554; AP 0,3264; Brier 0,1188. Limiar 0,13 escolhido na validação por acurácia balanceada. Matriz de confusão [[22335,16451],[1390,5953]], linhas observadas e colunas previstas. Precisão positiva 26,57%; sensibilidade 81,07%; especificidade 57,59%; acurácia 61,32%. Não destacar AUC omitindo os demais resultados.

## Limites de interpretação
Alvo Diabetes_binary não distingue tipos nem horizonte futuro; codificação original, ano e licença requerem reconciliação documental. Sem calibração clínica, ponderação amostral, validação temporal ou externa. Fontes de tipo 2 não validam o alvo. SHAP explica contribuições no modelo, não causas da doença. Não transformar escore em diagnóstico ou risco clínico.

# Evidências, geração e correções

## Recuperação
TF-IDF com filtro por fator e três trechos NIDDK/NIH de uma página: E01 idade, E02 IMC, E03 atividade física. Hipertensão não tem evidência elegível no conjunto e deve manter essa lacuna explícita até ampliação fundamentada. Ausência na base não significa ausência de associação no mundo.

## Geração com Ollama
qwen2.5:3b via /api/chat, formato JSON, temperatura zero e timeout de 90 s por chamada sequencial. Recebe nome do fator e documentos, não perfil completo nem SHAP; textos podem se repetir. Validação estrutural de claims e source_ids não confirma apoio semântico. Texto permanece rascunho sujeito à revisão humana.

## RAG e expertise
Recuperação com geração conectada compõe o fluxo RAG. Busca e sínteses fixas sozinhas não equivalem a geração. SHAP/XAI é explicabilidade. XAG foi citado pelo usuário como Expertise Augmented Generation; referência e método precisam ser confirmados com professor. Regras de engenharia não são expertise clínica coletada e validada.

## Correção do estado exportado
Antes, uma nova geração falha podia apagar o texto da tela e conservar generated_draft no resultado. A função generate_result agora limpa o estado antes da tentativa e só incorpora rascunhos após todas as chamadas. Testes cobrem sucesso seguido de falha, falha parcial e ausência de evidências. JSON e payload de feedback usam esse resultado limpo.

## Gráfico e avaliação
Campos internos factor/contribution_pp evitam interpretação indevida de pontos pelo Vega-Lite. Esquema validado e renderização isolada inspecionada com valores positivos, negativos e zero. Gráfico fica em seção expansível, com tabela. Avaliação deixa de iniciar em Concordo e exige seleção. Repetições ainda podem gerar novos registros; não existe política de coleta clínica.

# Testes e critérios de aceitação

## Evidência de execução
16 testes locais passaram em 20/11/2026, 0,358 s nesta execução. Modelo real usado no núcleo e AppTest. Log completo: docs/Resultado_testes.txt. Ruff não encontrou problemas na seleção F (imports/names); isso não é auditoria total de segurança ou qualidade.

## Cobertura
Cinco testes de núcleo: soma SHAP, entradas inválidas, recuperação, citações falsas e SQLite. Um teste de interface: temas/navegação/casos/feedback. Um de esquema do gráfico. Quatro de conector com HTTP simulado. Três de estado transacional. Dois de armazenamento inválido. Consultar código dos testes para limites precisos.

## Não verificado nesta execução
Ollama real, Windows, PostgreSQL e hospedagem pública. Chromium local não iniciou por restrição de socket, impedindo inspeção integral de layout e responsividade. Geração real e avaliação salva foram vistas anteriormente nas capturas de Daniel. AppTest não comprova CSS ou fidelidade visual. GitHub Actions foi preparado, não executado remotamente.

## Aceitação técnica pendente
Executar em Windows; conferir os três casos, soma, tabela e JSON; testar fontes, serviço Ollama desligado/ativo e respostas; revisar semântica; verificar feedback após reinício. Conferir temas em desktop e janela estreita com imagens aprovadas. Testar hospedagem e persistência se forem exigidas.

## Aceitação acadêmica pendente
Obter enunciado e construir matriz requisito/arquivo/evidência/responsável. Não assumir menções antigas a número de páginas, 22 tópicos ou duração da fala como requisitos confirmados. Concluir relatório acadêmico, divulgação e slides conforme professor; declarar uso de IA e limites. Não há nova consulta clínica ou validação externa nesta revisão.

# Instalação, dados e Git

## Windows
Extrair ZIP inteiro em pasta nova. Python 3.12 com launcher py. Abrir Iniciar_Windows.bat para instalar e iniciar. Para geração, instalar Ollama, executar ollama pull qwen2.5:3b no CMD, manter serviço ativo e abrir Iniciar_Com_Ollama.bat. Usar Local URL mostrada no terminal. Não colar comandos em app.py.

## Atualização e diagnóstico
Não substituir apenas app.py: há src/session.py, src/charts.py e assets/theme.css novos. Preservar instalação anterior e runtime. Se py falhar, revisar launcher e abrir terminal novo. Portas 8501/8502 podem ser instâncias diferentes. Conector configurado não significa serviço disponível; conferir ollama list. Testar_Windows.bat executa suíte após instalar.

## Persistência
SQLite em runtime/feedback.sqlite; FUNDAMENTO_DB altera caminho; DATABASE_URL seleciona PostgreSQL. Comentários até 500 caracteres. JSON do caso não é backup do banco. Não incluir dados pessoais. Sem autenticação/gestão de usuários concluídas. Hospedagem deve alcançar seu provedor de geração; localhost remoto não aponta ao notebook.

## Histórico verdadeiro
O primeiro commit importa o protótipo existente; os seguintes representam alterações reais da revisão de 20/11/2026. Autoria técnica Assistente do projeto, sem inventar autoria dos colegas ou datas passadas. Nenhum remoto foi criado ou publicado. ZIP inclui .git; o bundle preserva o mesmo histórico. Conferir HISTORICO_COMMITS.txt da entrega.

## Restaurar e continuar
Com Git instalado: git clone Fundamento.bundle Fundamento. Depois abrir a pasta e executar o iniciador. Para ver histórico: git log --oneline. Para publicar no próprio repositório, seguir docs/Git.md e configurar URL real. Novos commits do grupo devem usar a identidade de cada autor, sem reescrever os existentes.

# Transferência para o grupo

## Pacote e exclusões
Fundamento_3.zip contém código, testes, artefato do modelo, métricas, evidências, iniciadores, documentos e .git. Fundamento.bundle contém histórico portátil. Não incluem .venv, CSV original, modelo Ollama baixado, banco pessoal ou credenciais. Dependências devem ser instaladas em cada máquina. train.py sobrescreve modelo/métricas; não executar como teste rotineiro.

## Revisão em conversa comum
Anexar ZIP, este PDF e colar Prompt_revisao.txt. Se a plataforma não abrir ZIP, anexar Codigo_para_revisao.txt com cópia dos arquivos textuais. A outra IA não deve presumir acesso ao Work Mode, terminal, localhost ou arquivos antigos. Deve distinguir leitura de código, execução real e hipótese.

## Materiais que precisam acompanhar depois
Enunciado original, imagens visuais aprovadas, identificação confirmada da disciplina/professor e nomes dos colegas. O código registra as preferências de tema, mas referências visuais exatas não estão disponíveis neste pacote. Não preencher dados institucionais por suposição.

## Divisão sugerida
Pessoa A: código, testes, execução e eventual hospedagem. Pessoa B: fontes, rótulo, licenças e expertise com professor. Pessoa C: relatório acadêmico, divulgação e apresentação. Uma pessoa integra as mudanças. Cada integrante deve compreender e explicar sua parte.

## Demonstração sugerida
Caso B: explicar saída/referência sem diagnóstico; abrir gráfico; mostrar fonte e hipertensão sem suporte; gerar rascunho e explicar revisão humana; trocar para Caso A; salvar avaliação fictícia e baixar JSON; mostrar Método e limitações. Duração deve seguir o enunciado, ainda não confirmado.

## Conclusão da revisão
Foram corrigidas falhas identificadas e ampliados testes e documentação. A completude do protótipo distribuído não equivale a conformidade total da entrega acadêmica nem a produto clínico. Pendências e critérios estão registrados para a próxima revisão não depender da memória desta conversa.