# Fundamento 8 — interfaces do paciente e do médico

**Estado:** protótipo demonstrativo, com exames e perfis fictícios. Não é sistema assistencial real.

## Objetivo de experiência

- **Paciente:** leitura direta, respeitosa e sem termos desnecessários. Entrar por número de perfil e senha, visualizar um único cartão com situação (`SEM ALERTA NESTES EXAMES`, `ACOMPANHAR`, `ATENÇÃO`, `ALERTA` ou `SEM DADOS`), motivo em linguagem simples, orientação e data. Pode consultar **somente as datas** dos exames anteriores, sem gráficos, comparações complexas, SHAP, fontes extensas ou comentários médicos.
- **Médico:** primeiro vê o mesmo resultado resumido; depois, se desejar, confere os exames, a justificativa, as fontes SBD/ADA/NIDDK, os históricos e gráficos. Pode pesquisar por ID ou identificação fictícia, adicionar exames e registrar observações com autoria e data. Duas contas médicas de demonstração existem para testar a continuidade das notas.
- **Contas:** números `MED-DEMO`, `MED-002`, `DEMO-001`, `DEMO-002`. Senhas únicas e aleatórias são geradas no primeiro uso e escritas **apenas localmente** em `runtime/ACESSOS_DEMONSTRACAO.txt`, fora do ZIP e do Git. Login/senhas ficam armazenados no banco apenas como hashes PBKDF2 com salt, mas o protótipo **não** implementa todas as proteções necessárias para dados reais.

## Funções implementadas nesta revisão

| Parte | Arquivo | Verificação |
|---|---|---|
| Login local por perfil/senha | `src/auth.py`, `app.py` | `tests/test_auth.py` |
| Acesso do paciente limitado ao próprio perfil | `src/portal.py` e `src/auth.py` | `test_role_scoping` |
| Resumo enxuto sem gráficos para paciente | `src/presentation.py`, `src/portal.py` | Testes de saída e inspeção do código; conferir no Windows |
| Busca de pacientes pelo médico | `src/portal.py` | Conferir no Windows |
| Registro de exame exclusivamente pela área médica | `src/patients.py`, `src/portal.py` | `tests/test_patients.py` |
| Observações com autor e data | `src/patients.py`, `src/portal.py` | `tests/test_patients.py` |
| Exames antigos e linhas de evolução no médico | `src/portal.py` | Conferir no Windows |
| Histórico anterior, fontes e análise laboratorial | arquivos `src/clinical.py` e anteriores | Suíte de regressão clínica |

## Execução

No Windows: extrair tudo e abrir `Iniciar_Windows.bat`. Após começar, consultar `runtime/ACESSOS_DEMONSTRACAO.txt` (arquivo criado na máquina). **Não compartilhar credenciais nem carregar exames reais.** Para redefinir senha pelo terminal da pasta do projeto:

```bat
.venv\Scripts\python.exe -m src.auth reset DEMO-001
```

Para conferir a suíte:

```bat
Testar_Windows.bat
```

## Limites que o grupo deve declarar

- **Acesso de demonstração, não autenticação clínica:** faltam controle de autorização no serviço/banco para um sistema multiprofissional real, trilha de auditoria confiável, MFA, recuperação segura, gestão de consentimentos e compartilhamento, proteção em trânsito e em repouso, retenção, revisão de segurança e conformidade LGPD.
- **Sem diagnóstico clínico automático:** a tela apresenta comparações com critérios de exames, mas não distingue diabetes tipo 2 de outras formas; nem mesmo exames considerados normais eliminam todas as possibilidades de doença.
- **Sem percentual de risco de tipo 2:** não há modelo estatístico calibrado e validado com exames para essa finalidade. O modelo histórico com SHAP fica separado e não deve ser usado como probabilidade clínica.
- **Sem Chat RAG individual ligado ao perfil:** há apenas funções experimentais de geração no modelo histórico; não declarar implantado no prontuário.
- **Sem publicação confirmada:** ao publicar futuramente, não expor o arquivo de senhas ou dados de saúde e confirmar que o servidor de Streamlit e o banco são persistentes.
- **Documentos acadêmicos anteriores:** versões do relatório, plano e slides no pacote podem se referir ao fluxo antigo. Atualizar antes da entrega, incluindo telas e evidências realmente verificadas.

## Testes locais nesta sessão

A descoberta de `54` testes contém `52` que passaram e `2` que não puderam ser importados devido à ausência local de `streamlit` e `altair`. **Não há execução integrada de navegador Streamlit verificada aqui.** São necessárias inspeção visual e execução no Windows para declarar aceite final.

## Roteiro de aceite no Windows

1. O primeiro início gera `runtime/ACESSOS_DEMONSTRACAO.txt` e nenhuma senha fixa aparece no código/repositório.
2. A conta `DEMO-001` vê somente o próprio resultado e datas, não contém gráficos, notas ou formulário de exames.
3. A conta `DEMO-002` **não** vê `DEMO-001`, inclusive ao modificar interações de navegação.
4. `MED-DEMO` pode buscar `DEMO-001`, ver análise resumida e abrir detalhes, histórico, fontes.
5. `MED-002` pode acrescentar uma nota e `MED-DEMO` a vê com autor e data.
6. O médico pode cadastrar novo paciente fictício; anotando a senha única, o paciente acessa apenas o novo perfil.
7. O médico adiciona novos exames com condições informadas; o último resultado e o histórico mudam corretamente após salvar.
8. Exames faltantes, discordantes e valores inválidos não se tornam automaticamente certeza de diabetes ou de ausência de doença.
9. Testar os temas claro/escuro em desktop e tela estreita. Verificar contraste, rolamento e tamanho do cartão de resultado.
10. Publicação, IA por perfil, revisão clínica e auditoria de segurança devem permanecer **pendências** até comprovadas.
