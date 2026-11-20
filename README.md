# Fundamento 2

Primeira versão executável do protótipo acadêmico. Não está pronta para uso clínico nem representa integração com a Unimed.

## Começar no Windows

1. Instale Python 3.12 pelo site oficial: https://www.python.org/downloads/windows/
2. Extraia o ZIP inteiro. Não execute de dentro do arquivo compactado.
3. Abra a pasta Fundamento_2.
4. Clique duas vezes em Iniciar_Windows.bat. Na primeira execução ele cria um ambiente isolado e instala as dependências.
5. Aguarde o navegador abrir. Se necessário, use o endereço local que o terminal mostrar, normalmente http://localhost:8501.
6. Selecione um caso fictício e clique em Analisar caso. Confira contribuições, fontes e fator sem evidência; salve uma avaliação.
7. Não feche o terminal enquanto estiver usando o aplicativo. Para encerrar, Ctrl+C.

Se der erro, copie o texto completo do terminal para o chat. Não envie senhas ou chaves.

## Comandos equivalentes

Dentro da pasta do projeto:

    py -3.12 -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    .venv\Scripts\python.exe -m streamlit run app.py

Linux/macOS com Python 3.12:

    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python -m streamlit run app.py

## O que está implementado e testado

- Modelo de árvore de decisão treinado sobre o arquivo público UCI CDC Diabetes Health Indicators.
- Quatro variáveis: categoria de idade, IMC, atividade física e hipertensão relatada.
- SHAP calculado sobre o modelo real, com verificação da reconstrução da saída.
- Recuperação TF-IDF com filtro por fator em três fragmentos documentais.
- Fontes e trechos acessíveis; ausência de evidência para hipertensão na base inicial é explícita.
- Três casos fictícios fixos, sem formulário de prontuários reais.
- Avaliações persistidas em SQLite local; exportação do registro do caso.
- Regras explícitas de validação, abstenção e rastreabilidade.
- Testes de núcleo e interface Streamlit sem navegador gráfico.

## O que ainda NÃO foi concluído

- O aplicativo não está publicado. Streamlit/Python não roda em hospedagem estática como GitHub Pages.
- A geração Ollama foi observada no Windows de Daniel em etapa anterior; não foi repetida na validação deste pacote. A configuração é local a cada computador.
- Busca e sínteses cadastradas isoladas não são RAG completo; geração com documentos está disponível quando Ollama funciona.
- Conector PostgreSQL preparado, mas banco remoto não configurado nem testado.
- Expertise clínica não foi coletada nem validada com médicos. As regras existentes são de engenharia, não XAG clínico validado.
- Revisão clínica, semântica das respostas geradas, licença da base original e codificação original do rótulo precisam de conferência.
- Sem auditoria de acessibilidade visual, segurança para produção ou validação externa.
- O pacote não inclui relatório final, plano de disseminação ou slides da entrega.

## Sobre o rótulo e os números

O arquivo obtido tem 253.680 linhas, 21 entradas originais, ID e Diabetes_binary. Não tem valores ausentes. O modelo utiliza apenas quatro entradas. Não há HbA1c, glicemia ou histórico familiar nessas quatro entradas; não inventar essas variáveis.

A descrição UCI informa classe 1 = pré-diabetes ou diabetes, mas seu resumo contém inconsistências sobre quantidade de variáveis e classes. Até conciliar com o material original, o produto usa a expressão classe 1 de Diabetes_binary. Não dizer que prevê diabetes tipo 2 ou risco em cinco anos.

Treino, validação e teste são separados por grupos de perfis idênticos nas quatro entradas. O limiar de avaliação foi escolhido na validação para maximizar acurácia balanceada; não é limiar médico. Os resultados reais estão em assets/metrics.json. Não há avaliação externa nem calibração clínica.

O percentual é a saída estatística do modelo da base, não a probabilidade validada de doença de uma pessoa. SHAP mostra contribuição para esse modelo, não causalidade. Evidências sobre fatores de diabetes tipo 2 dão contexto geral e não validam o alvo do modelo.

## Onde cada coisa está

- app.py: interface e fluxo.
- src/core.py: validação, SHAP e busca de trechos.
- src/storage.py: avaliações e persistência.
- src/generation.py: conector opcional e validação estrutural de geração.
- train.py: aquisição do CSV e treinamento reproduzível.
- assets/model.joblib: modelo treinado neste projeto (não carregar artefatos de terceiros sem confiança).
- assets/metrics.json: resultados reais e hash do CSV.
- assets/evidence.json: sínteses, trechos curtos e fontes.
- assets/rules.json: regras e estado de revisão.
- assets/uci_metadata.json: metadados recuperados da UCI.
- tests/: testes automatizados.
- docs/: relatório de continuidade, prompt, pendências, testes e registro de IA.

## Geração opcional: preparar depois da primeira execução

O conector segue POST /api/chat do Ollama. Não instala nem baixa um modelo automaticamente. Depois de escolher e testar um modelo, o operador pode definir OLLAMA_MODEL e OLLAMA_URL no servidor; o padrão de URL local é http://localhost:11434.

No Windows, antes de iniciar a aplicação, em um terminal com Ollama já instalado e o modelo já disponível:

    set OLLAMA_MODEL=NOME_EXATO_DO_MODELO_INSTALADO
    Iniciar_Windows.bat

Não copie o nome acima literalmente: é um marcador. Não exponha seu servidor local publicamente sem controle de acesso. Na hospedagem, localhost é o próprio servidor de hospedagem, não seu notebook.

O gerador recebe apenas o nome do fator e trechos, não um paciente real. Exige JSON com claims e source_ids. Citações ausentes ou desconhecidas bloqueiam a resposta. Esse controle é estrutural, não comprova suporte semântico. Textos gerados ficam rotulados como rascunhos para revisão. Falha da API não produz resposta simulada.

## Persistência e publicação

Localmente, os registros ficam em runtime/feedback.sqlite, ignorado pelo Git. Não use esse arquivo para persistência permanente em Streamlit Community Cloud.

O conector PostgreSQL usa DATABASE_URL no ambiente/secrets. Use credencial restrita, TLS e base de demonstração. A aplicação cria a tabela feedback se permitido. Não colocar credenciais no repositório. O conector remoto ainda precisa de teste de gravação/leitura e de avaliação de permissões antes de publicar.

Para Streamlit Community Cloud: criar repositório com os arquivos do projeto na raiz; selecionar repositório, ramo e app.py; selecionar Python 3.12; instalar dependências; configurar segredos no painel. Revisar licença e rótulo antes de publicar o modelo. Testar o link fora da conta do autor. Sem DATABASE_URL, os registros locais da hospedagem podem desaparecer.

## Testar e reproduzir

Na raiz do projeto:

    python -m unittest discover -s tests -v

Treinamento opcional, não necessário para executar os testes:

    python train.py

O segundo comando baixa novamente a fonte e sobrescreve o modelo e métricas. O CSV baixado fica em runtime e não integra o pacote. Conferir o hash se a fonte mudar. O conjunto original não foi incluído no ZIP; a licença deve ser conferida na fonte original antes da publicação e redistribuição.

## Referências de implementação

UCI: https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
Fonte original indicada pela UCI: https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset
NIDDK: https://www.niddk.nih.gov/health-information/diabetes/overview/risk-factors-type-2-diabetes
SHAP: https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html
Ollama: https://docs.ollama.com/api/chat
Streamlit: https://docs.streamlit.io/deploy/streamlit-community-cloud

Fontes consultadas em 16/11/2026. Revisar fontes clínicas atuais com o responsável pela frente B.


## Entrega de continuidade
Leia COMECAR_AQUI.txt, docs/Relatorio_continuidade.pdf e docs/Prompt_continuidade.txt. Interface atualizada; testes registrados em docs/Resultado_testes.txt. Visual integral e geração local devem ser conferidos em cada computador.
