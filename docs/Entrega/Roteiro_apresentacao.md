# Fundamento — fala e roteiro de 15 minutos

**Finalidade:** apresentar um protótipo funcional e inovador de *interpretação explicável de exames fictícios*, não diagnóstico automatizado. Três integrantes — preencher os nomes reais antes de usar.

## Pessoa 1 — slides 1 a 4 (0:00–4:30)

**Slide 1.** “Somos um grupo de três integrantes e desenvolvemos o Fundamento. Nosso protótipo organiza exames relacionados ao diabetes e apresenta o resultado de forma diferente para médico e paciente, sempre com dados fictícios.”

**Slide 2.** “O problema que identificamos é a quantidade de números isolados que chegam ao usuário, sem mostrar de forma clara o significado e a confiabilidade da conclusão. Também há o risco de ferramentas digitais transmitirem certeza indevida ou porcentagens sem validação.”

**Slide 3.** “O médico abre o perfil de um paciente fictício, consulta resultados anteriores, adiciona um exame e acessa justificativas e fontes. O paciente vê apenas um resumo e as datas. São duas interfaces sobre a mesma estrutura de registro.”

**Slide 4.** “A análise do protótipo utiliza critérios publicados pela Sociedade Brasileira de Diabetes e referencia ADA e NIDDK. Os valores não são interpretados sem conferir as condições de coleta. O programa informa quando dados estão ausentes ou inconclusivos, sem afirmar que identificou sozinho o diabetes tipo 2.”

## Pessoa 2 — slides 5 a 8 e demonstração local (4:30–10:30)

**Antes de apresentar:** deixe o Streamlit local aberto pelo atalho `APRESENTAR_WINDOWS.bat`. Use modo claro ou escuro, com perfil DEMO-001 já preparado. Não dependa de senha para a apresentação.

**Slide 5 / demonstração ao vivo (4:30–8:30):** “Vou abrir a versão local demonstrativa. Escolho *Médico*. No perfil DEMO-001, o sistema mostra a conclusão mais recente, valores de glicemia e HbA1c e um histórico em três datas. Abrindo os detalhes, verifico a justificativa e as fontes. Abaixo, posso registrar um exame fictício e uma nota de acompanhamento que ficará com autor e data. Agora saio e entro como *Paciente*: a mesma pessoa vê apenas a mensagem resumida, sem gráficos ou detalhes técnicos.”

**Slide 6.** “Quando não há informações suficientes, quando exames discordam ou quando há condições especiais, o sistema deve dizer isso claramente. A ausência de probabilidade validada é intencional, não um número omitido.”

**Slide 7.** “O código é dividido em módulos. A interface é feita com Streamlit; o módulo `patients.py` guarda perfis e histórico; `clinical.py` aplica regras; `portal.py` monta as duas áreas. O modelo histórico SHAP está separado e não é usado para calcular a conclusão laboratorial.”

**Slide 8.** “Registramos verificações automatizadas de regras, persistência, acesso demonstrativo e tratamento de entradas. O navegador real no Windows e a URL pública exigem comprovação à parte. Nossa aplicação permanece acadêmica e não foi validada para uso clínico.”

## Pessoa 3 — slides 9 a 12 (10:30–15:00)

**Slide 9.** “O diferencial incremental é integrar histórico, resumo para paciente, análise aprofundada para médico, notas e explicação com fontes, sem forçar resposta quando faltam evidências. O benefício deve ser verificado em testes com usuários convidados; não alegamos adoção real.”

**Slide 10.** “Nossa evolução em doze meses priorizaria validação de usabilidade, segurança, revisão de documentos, avaliação com profissionais e só depois qualquer possibilidade de integração clínica ou modelo probabilístico.”

**Slide 11.** “O limite é importante: não mostramos diagnóstico automático de tipo 2, não estimamos risco futuro ou probabilidade individual e não trabalhamos com exames de pacientes reais. A demonstração pública, quando publicada, será apenas de consulta a dados sintéticos.”

**Slide 12.** “As referências são públicas, e a documentação descreve o uso de ferramentas de IA. Estamos prontos para explicar o código, os testes e, principalmente, o que o aplicativo não consegue comprovar.”

## Treino e perguntas

- Tempo dos três blocos: **4min30 + 6min + 4min30 = 15min**; cronometrar e ajustar à velocidade real do grupo.
- Preparar uma captura REAL das telas e da URL publicada para contingência. Um vídeo conceitual não prova funcionamento.
- **‘Qual probabilidade de diabetes tipo 2?’** Não há estimativa validada no protótipo; a análise atual aplica critérios de exames e não identifica automaticamente o subtipo.
- **‘Tem RAG funcionando no prontuário?’** Não. Há fontes clínicas vinculadas às regras; a recuperação e geração Ollama antigas são experimentais e separadas.
- **‘Como garantem privacidade?’** Só usamos pacientes fictícios. Vitrine pública é somente leitura; autenticação segura e regulamentação seriam pré-requisitos para dados reais.
- **‘Qual o potencial inovador?’** Duas linguagens, histórico longitudinal, justificativa rastreável e indicação explícita de dados insuficientes no mesmo fluxo.
