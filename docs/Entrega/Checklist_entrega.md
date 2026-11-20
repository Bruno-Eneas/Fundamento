# Fundamento — revisão final de escopo e roteiro de entrega
**20 de novembro de 2026 · Versão de trabalho 10 · Dados 100% fictícios**

## 1. Produto que o grupo demonstrará
Uma plataforma **educacional** de interpretação de exames laboratoriais com dois níveis de linguagem. O médico pesquisa um perfil fictício, encontra o resultado principal, revisa o histórico, consulta fontes e registra observações de continuidade. O paciente vê um resultado objetivo e as datas, sem gráficos. A máquina aplica critérios explícitos e abstém-se quando não há suporte. Não estima probabilidade clínica individual nem determina automaticamente o subtipo do diabetes.

## 2. Caminho de apresentação em 5 minutos
1. **00:00–00:35:** executar `APRESENTAR_WINDOWS.bat` (preferencialmente já aberto) e mostrar os dois acessos simplificados; explicar que dispensam senha *somente na demonstração local*.
2. **00:35–01:30:** clicar **Entrar como médico**, selecionar `DEMO-001`; ler a conclusão no cartão, os dois exames mais recentes e os links SBD/ADA/NIDDK.
3. **01:30–02:35:** abrir **Consultar evolução e histórico completo**; mostrar o histórico de 3 datas de glicemia e HbA1c.
4. **02:35–03:30:** abrir **Adicionar exame ao histórico** e demonstrar o formulário, sem precisar preencher na hora. Mostrar nota médica fictícia com autor/data; acrescentar uma observação curta se houver tempo.
5. **03:30–04:20:** **Sair da conta** e **Ver área do paciente**; mostrar que somente o próprio perfil de exemplo aparece e que a comunicação foi simplificada, sem gráficos.
6. **04:20–05:00:** explicar o diferencial, a fonte primária e o limite: *sem porcentagem validada e sem diagnóstico definitivo*. Não alegar que é um serviço para pacientes reais.

Se o navegador falhar durante a apresentação, **não mostrar um vídeo conceitual como teste**. Apresentar capturas reais previamente produzidas no Windows e esclarecer que são evidências de uma execução anterior; manter a demonstração ao vivo como prioridade.

## 3. Funcionalidades: mostrar x deixar como plano
| Mostrar na banca | Deixar como extensão futura |
| --- | --- |
| Médico: pesquisa de paciente fictício | Integração com prontuários reais |
| Histórico de exames e notas por paciente | Identificação médica certificada e compartilhamento entre instituições |
| Resultado claro para médico/paciente | Chat RAG integrado ao histórico |
| Critérios e links SBD/ADA/NIDDK | Modelo probabilístico clinicamente validado para DM2 |
| Informação ausente ou divergente | Leitura automática irrestrita de exames e PDFs escaneados |
| Dois temas com pinheiros | Aplicação clínica e estudos de eficácia |

**Não colocar a árvore histórica como o resultado principal.** Ela usa idade, IMC, atividade física e hipertensão; não usa glicemia/HbA1c e não valida risco clínico.

## 4. Matriz do enunciado (resumo)
| Obrigação oficial | Arquivo/evidência | Situação a conferir |
| --- | --- | --- |
| App funcional e código completo | `app.py`, `src/`, `assets/`, `tests/` | Testar na máquina final e capturar evidências |
| Interface utilizável, caso de uso e organização | Áreas médico/paciente, SQLite, módulos | Inspecionar desktop/celular e dois temas |
| **Publicação pública** | URL Streamlit, teste em navegador anônimo | **PENDENTE; exige prova antes de marcar concluído** |
| Relatório técnico 15–25 páginas / 22 tópicos | `docs/Entrega/Relatorio_Fundamento.docx/.pdf` | Atualizar dados da equipe e imagens reais; conferir requisitos |
| Plano de disseminação 5–10 páginas | `docs/Entrega/Plano_Fundamento.docx/.pdf` | Conferir cenário e estratégia; incluir URL real |
| Pitch 15 min + 20 min arguição | `docs/Entrega/Apresentacao_Fundamento.pptx`, roteiro | Ensaiar no cronômetro; dividir falas dos três integrantes |
| Declarar uso de IA | `docs/Uso_de_IA.md` e relatório | Conferir ferramentas, trechos e alterações efetivas |

O enunciado atribui 35 pontos a inovação e originalidade, 20 a relevância, 20 a qualidade técnica, 10 a viabilidade/escalabilidade, 10 a disseminação e 5 à apresentação. Prevê penalidade de 10 pontos por ausência de publicação pública, entre outras penalidades.

## 5. Publicar sem divulgar dados reais
O Streamlit Community Cloud hospeda aplicações Python. Na configuração do app, habilitar `FUNDAMENTO_PUBLIC_SHOWCASE=1` por **configuração de ambiente/segredos**, nunca publicar `runtime/` e nunca ativar a demonstração local editável. Esse modo dá acesso de leitura a perfis **fictícios** sem senhas, deliberadamente: a vitrine pública não contém prontuários reais, não permite registrar exames ou notas e não deve ser anunciada como um sistema de saúde em funcionamento. Testar também com janela anônima e celular.

**Atenção:** salvar dados com SQLite local não garante continuidade na hospedagem gratuita. O histórico dos perfis predefinidos pode ser reconstruído no início da aplicação; não prometer persistência entre reinícios na vitrine. Para um sistema real seriam necessários autenticação segura, autorização por vínculo profissional, auditoria de acesso, consentimento/base legal, infraestrutura persistente e revisão regulatória.

## 6. Critérios de aceite, em ordem
- [ ] `APRESENTAR_WINDOWS.bat` abre e os dois botões mostram perfis diferentes (local).
- [ ] `DEMO-001` tem 3 exames e ao menos uma observação fictícia; o médico vê gráfico, justificativa e fontes.
- [ ] O paciente não vê notas médicas, gráficos ou acesso a outros perfis.
- [ ] Adicionar exame fictício na área médica atualiza o cartão e o histórico, sem corromper dados.
- [ ] Formulário aceita ausência de exames e conflito sem inventar conclusão; gestação e interferência provocam abstenção conforme regras implementadas.
- [ ] O tema claro e o escuro funcionam em telas largas/estreitas.
- [ ] `Testar_Windows.bat` passa com as dependências instaladas; registrar log real.
- [ ] Existe URL pública navegável com apenas dados fictícios e sem botão de escrita.
- [ ] Atualizar os documentos com capturas REAIS, link publicado, nomes e professor.
- [ ] Realizar ensaio de 15 minutos, distribuir 3 falas e preparar respostas para perguntas técnicas e éticas.

## 7. Como responder às dúvidas da banca
**"O aplicativo dá diagnóstico de diabetes tipo 2?"** Não. Ele sinaliza resultados compatíveis com critérios laboratoriais e informa quando falta confirmação; o tipo requer avaliação clínica.

**"Qual é a precisão do modelo?"** A árvore histórica possui métricas internas documentadas, mas não recebe exames e não pode ser usada para afirmar precisão clínica do módulo principal. O módulo principal aplica faixas oficiais, não é um classificador probabilístico.

**"Onde está a IA?"** Há um modelo de decisão e explicação SHAP em uma seção técnica opcional, e um gerador Ollama experimental separado. O resultado principal de exames é determinado por regras e fontes explícitas. Não há chat com RAG vinculado ao paciente. A contribuição científica aqui é também a escolha consciente de explicar e saber não responder.

**"Qual é a inovação?"** Proposta incremental: histórico + duas camadas de linguagem + justificativa rastreável + abstenção + notas de acompanhamento, em um fluxo acessível. Originalidade, eficácia e adoção ainda precisam de avaliação externa.
