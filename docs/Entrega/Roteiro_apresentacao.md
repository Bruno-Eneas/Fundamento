# Fundamento — roteiro de 15 minutos

**Pessoa A — 0:00 a 5:00 — problema e produto (slides 1–4)**

Explique que o usuário informa exames e vê a interpretação rastreável. Não prometa diagnóstico. Mostre as quatro entradas laboratoriais principais e que critérios SBD 2026, ADA 2026 e NIDDK servem de referências. Declare que o foco do produto é clareza, segurança e abstenção.

**Pessoa B — 5:00 a 10:00 — demonstração e arquitetura (slides 5–8)**

Abra a aba Exames e demonstre exemplos A, B e C. Indique a diferença entre faixa, confirmação e diagnóstico. Mostre código em `src/clinical.py` e links para as fontes. Explique que a árvore histórica com SHAP é opcional, não a parte clínica. Destaque testes específicos realizados e o que ainda não foi verificado em Windows/produção.

**Pessoa C — 10:00 a 15:00 — inovação, viabilidade e encerramento (slides 9–12)**

Apresente o diferencial incremental, canais acadêmicos, hipóteses de evolução em 12 meses, privacidade, publicação obrigatória e limites. Explique a ausência de probabilidade individual validada como decisão de engenharia responsável. Encaminhe para arguição: o professor prevê 20 minutos de perguntas.

## Perguntas prováveis da banca

**Por que não aparece uma probabilidade?** O modelo original não usa exames e não está validado clinicamente. Percentuais não podem ser improvisados a partir dos limiares. A etapa probabilística requer base adequada e validação externa.

**O sistema diagnostica diabetes?** Não. Relaciona valores fictícios a critérios de diretrizes, mas confirmação e avaliação individual cabem ao profissional.

**Qual é a inovação?** Integra entrada, validade dos dados, critérios, fontes, explicações e abstenção em uma interface auditável. Precisamos demonstrar diferencial com testes e comparações, não apenas declarar inovação.

**Há pacientes reais ou parceria?** Não. Nenhuma parceria oficial ou avaliação médica está comprovada.

**Como tratar exames em PDF?** Leitura experimental de PDFs textuais fictícios e sem identificação; operador confirma os valores. Nada de upload de prontuários reais nesta fase.

**O que falta para cumprir o enunciado?** URL pública, testes finais em máquina do grupo, confirmação dos integrantes e prazo, ensaio e revisão documental/humana.
