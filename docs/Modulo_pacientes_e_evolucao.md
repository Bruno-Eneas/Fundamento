# Fundamento — Perfis, histórico e evolução médica (demonstração)

## Visão para demonstrar ao professor

Este módulo é **exclusivamente demonstrativo**, com perfis e valores fictícios.
Não implementa login, autenticação, autorização ou prontuário clínico seguro.
A seleção “Médico demonstrativo” ou “Paciente demonstrativo” **não é controle de acesso**.

### Acesso do paciente (fictício)
- Visualiza o perfil fixo `DEMO-001` e o último resumo laboratorial em linguagem simples.
- Consulta o histórico e gráficos de evolução de HbA1c e glicemia de jejum.
- Digita novos valores, data do exame e condições, ou pré-preenche com PDF textual fictício.
- Não vê notas internas dos profissionais.
- A informação é educativa e não confirma diabetes tipo 2 nem informa probabilidade individual.

### Acesso do médico (fictício)
- Seleciona qualquer **perfil de demonstração** já existente ou cadastra um novo perfil fictício.
- Consulta resultados, fontes, sugestões condicionais e a série histórica.
- Registra `Observação`, `Pendência` ou `Plano de acompanhamento`.
- Cada nota registra data em UTC e origem “Médico demonstrativo”, sem possibilidade de edição ou exclusão pela interface.
- Pode registrar novos resultados laboratoriais associados ao perfil.

### Dados de demonstração
- `DEMO-001`: três datas fictícias; o último registro tem glicemia de jejum 132 mg/dL e HbA1c 6,8%.
- `DEMO-002`: exames fictícios em faixas inferiores à intermediária.
- Notas e exames novos usam SQLite no arquivo `runtime/demo.sqlite` (ignorado pelo Git).
- `FUNDAMENTO_DEMO_DB` muda o caminho da base demo em testes locais.
- Banco de feedback (`runtime/feedback.sqlite`) é diferente do banco de perfis.

## O que foi implementado

- `src/patients.py`: esquema SQLite, perfis, exames e notas, verificação de entradas e isolamento por identificador de perfil.
- `src/portal.py`: telas de paciente e médico, gráficos, formulários e observações.
- `app.py`: menu de papel simulado e navegação adicional.
- `tests/test_patients.py`: testes de semente idempotente, histórico, validação, notas e isolamento do banco.

## Limites essenciais para a banca

1. **Não usar pacientes reais**, com nome, CPF, imagens de exames identificáveis ou informações clínicas sensíveis.
2. O protótipo não possui contas de usuário, autenticação multifator, autorizações por equipe, consentimentos, criptografia, política de retenção ou trilhas de auditoria imutáveis.
3. A nota “Médico demonstrativo” não equivale a identificação formal, assinatura eletrônica ou prontuário de saúde regulamentado.
4. As regras laboratoriais identificam faixas e necessidade de revisão médica; não estabelecem tipo 2 por si mesmas.
5. O percentual individual **não está disponível**. O antigo modelo em `Análise` é separado, não treinado com resultados laboratoriais.
6. A versão ainda não foi executada com Streamlit real no ambiente de criação; repetir a suíte e o fluxo completo no Windows do grupo.
7. Uma futura hospedagem pública só deve usar dados fictícios. Usuários podem burlar a seleção visual de papéis; **não é seguro para dados reais**.

## Checklist manual no Windows

1. Extrair o ZIP, instalar Python 3.12 e executar `Iniciar_Windows.bat`.
2. Em “Visualizar como”, selecionar **Paciente demonstrativo**. Confirmar que mostra só `DEMO-001`, histórico e envio de exames fictícios, sem observações internas.
3. Salvar um exame fictício com data e conferir que a análise e o histórico mudam.
4. Selecionar **Médico demonstrativo** e abrir `DEMO-001` e `DEMO-002`; confirmar que não misturam exames ou notas.
5. Criar novo perfil fictício, selecioná-lo e registrar um exame.
6. Registrar observação como médico; recarregar o navegador e confirmar persistência e autoria demonstrativa.
7. Alternar tema claro/escuro, verificar botões/contraste e largura de tela reduzida.
8. Rodar `Testar_Windows.bat` e guardar log; não declarar que todos passaram antes de executar.
9. Testar o PDF com arquivo exclusivamente fictício, e conferir manualmente valores extraídos antes de salvar.

## Próximas etapas para uso sério (não implementadas)

- Identidade real do profissional e do paciente, autenticação forte e acesso estritamente autorizado por vínculo clínico.
- Trilha de auditoria robusta (autor real, alterações, justificativa e acesso ao prontuário), controle de versões e política de retenção.
- Revisão por profissional de saúde, avaliação de riscos, proteção de dados, privacidade e governança institucional.
- Chat RAG ligado ao **histórico autorizado**, com fontes clínicas e filtros contra respostas não fundamentadas.
- Integração com prontuários reais apenas depois de revisão legal, técnica e de segurança.
- Estimativa probabilística somente após desenvolvimento, calibração e avaliação independente de modelo específico.
- Atualização do relatório acadêmico, plano e slides para refletir essas mudanças **de fato implementadas**.
