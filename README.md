# Fundamento

Protótipo acadêmico de explicabilidade e consulta documental sobre indicadores de diabetes. Perfis fictícios; não confirma nem descarta doença. Não representa sistema oficial da Unimed.

## Começar no Windows

1. Extraia o ZIP inteiro, inclusive subpastas, para uma pasta nova.
2. Instale Python 3.12 com launcher `py`. Abra `Iniciar_Windows.bat`.
3. Para geração local, instale Ollama separadamente e execute no CMD `ollama pull qwen2.5:3b`. Mantenha o serviço ativo e abra `Iniciar_Com_Ollama.bat`.
4. Use a **Local URL** exibida no terminal. Mantenha o terminal aberto. Ctrl+C encerra aquela instância.
5. Caso B abre calculado. Troque o perfil, abra fontes e “Ver gráfico de contribuições SHAP”. A geração só ocorre ao clicar no botão. Escolha explicitamente a avaliação antes de salvar.

Não cole comandos de terminal em app.py. Para Linux: `bash Iniciar_Linux.sh` (script incluído; não testado como instalador nesta entrega).

## Testar

No Windows já instalado, abra `Testar_Windows.bat` ou execute na raiz:

```bat
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Nos demais ambientes instalados: `python -m unittest discover -s tests -v`. A suíte não exige Ollama nem PostgreSQL. Os testes HTTP são simulados. Veja docs/Verificacoes.md e docs/Resultado_testes.txt.

## Arquitetura

- app.py: interface, casos, navegação e exportação.
- assets/theme.css: temas petróleo e branco/esmeralda; pinheiro ilustrativo.
- src/core.py: validação, modelo, SHAP e recuperação TF-IDF.
- src/charts.py: especificação compartilhada do gráfico.
- src/session.py: geração transacional e limpeza de resultados antigos.
- src/generation.py: requisição Ollama e validação estrutural das citações.
- src/storage.py: SQLite e conector PostgreSQL.
- assets/: modelo, métricas, regras, evidências e metadados.
- tests/: testes do núcleo, interface, gráfico, geração, estado e armazenamento.
- docs/: relatório técnico de continuidade, plano do grupo, registro de IA e prompt.

## Entradas e limites

Árvore de profundidade 4, mínimo de 500 registros por folha; Age (categoria, não idade em anos), BMI, PhysActivity e HighBP. Há somente três perfis fictícios. Não existem entradas de glicemia, HbA1c ou histórico familiar.

SHAP explica a saída do modelo, não causalidade clínica. O alvo Diabetes_binary não distingue tipos ou horizonte futuro. A descrição original e a licença continuam pendentes de reconciliação. Fontes NIDDK falam de diabetes tipo 2 e oferecem contexto geral. Não chamar o escore de risco clínico validado.

Busca TF-IDF por fator com três trechos cadastrados de uma fonte institucional. Hipertensão não tem suporte no conjunto atual; isso não prova ausência de associação. Geração recebe fatores e documentos, não prontuário nem valores SHAP. IDs são verificados, apoio semântico não. A expertise clínica não foi coletada/validada. XAG não é sinônimo de SHAP.

## Persistência e configuração

`OLLAMA_MODEL=qwen2.5:3b`; `OLLAMA_URL` padrão `http://localhost:11434`. Configuração não garante serviço disponível. São chamadas sequenciais por fator, com timeout de 90 segundos cada.

Sem `DATABASE_URL`, avaliações ficam em `runtime/feedback.sqlite`; `FUNDAMENTO_DB` pode mudar o caminho. Comentários até 500 caracteres. Não inserir dados pessoais. O botão de exportação gera JSON do caso, não backup do banco. Preserve runtime ao atualizar.

`DATABASE_URL` seleciona PostgreSQL. Nunca versionar segredos. Banco remoto, autenticação e implantação não foram concluídos. Servidor remoto não acessa automaticamente o Ollama do notebook. GitHub Pages não executa Streamlit/Python.

## Treinamento (opcional, destrutivo para os artefatos atuais)

`python train.py` baixa o CSV e sobrescreve modelo/métricas; não é necessário para executar a demonstração ou os testes. O CSV não está incluído. Conferir licenças antes de redistribuir dados/modelos. Hash, divisão e desempenho completos em assets/metrics.json.

## Histórico Git

O ZIP inclui `.git` e o arquivo Fundamento.bundle preserva o mesmo histórico. Os commits foram criados em 20/11/2026: importação do protótipo existente e mudanças reais desta revisão. Não representam dias passados de desenvolvimento. Autor técnico: Assistente do projeto; não há atribuição fictícia aos integrantes. Veja docs/Git.md.

## Antes da entrega acadêmica

Faltam enunciado original e imagens de referência aprovadas para fechar conformidade acadêmica e visual. Relatório de continuidade não é relatório acadêmico final. Conferir docs/Proximas_tarefas.md. Não afirmar publicação, parceria operacional, validação médica ou ausência de alucinações.
