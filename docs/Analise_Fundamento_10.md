# Auditoria objetiva — Fundamento 10
20/11/2026 | Base: `Fundamento_9.zip`, `docs/Enunciado.pdf`, código e materiais da versão atualizada.

## Parecer
**O projeto tem uma base implementada suficiente para uma demonstração acadêmica relevante, mas não há comprovação de entrega completa.** O principal risco de nota é ausência de URL pública, seguida por falta de evidências reais e documentos que não descrevam a mesma versão apresentada.

## Produto mínimo recomendado
**Médico:** pesquisar `DEMO-001`, ler o resultado resumido, abrir histórico de três exames, verificar fontes e registrar nota fictícia. **Paciente:** entrar no próprio perfil fictício e ver resumo simples, última data e histórico de datas sem gráficos. **Em ambos:** não afirmar diagnóstico de diabetes tipo 2 nem porcentagem sem modelo validado.

## Achados por arquivo
| Severidade | Local | Constatação | Resolução / verificação |
| --- | --- | --- | --- |
| Alta (entrega) | Execução / deployment | Publicação pública exigida; URL não encontrada no pacote. | Publicar vitrine Streamlit somente leitura; testar externamente e inserir URL nos materiais. |
| Alta (segurança) | `src/auth.py` / `src/portal.py` | Senha local demonstrativa não equivale a conta médica segura; não usar com dados reais. | `APRESENTAR_WINDOWS.bat` sem senha só local; vitrine pública sem escrita. Validar com dados sintéticos. |
| Alta (método) | `src/clinical.py` | Regras comparativas de exames não classificam automaticamente o subtipo nem produzem probabilidade clínica. | Apresentar corretamente como interpretação laboratorial e decisão de não estimar probabilidade. Conferir com médico. |
| Média (usabilidade) | `app.py` | Login anterior exigia descobrir senhas em runtime, dificultando a banca. | Modo de apresentação local com dois botões, sem alterar login normal. |
| Média (persistência) | `src/patients.py` | SQLite funciona localmente; hospedagem gratuita não garante persistência entre reinícios. | Vitrine somente leitura com perfis sem dados reais, e registro de exame apenas no modo local. |
| Média (evidência) | `docs/Entrega/Relatorio_Fundamento.docx` | Capturas antigas de prévia HTML, não do app atual. | Capturar telas reais Windows e atualizar antes de entregar. |
| Média (documentação) | `README.md`, plano e slides | Material anterior se concentrava em casos avulsos, enquanto código atual possui dois papéis e histórico. | Conteúdo atualizado; professor/integrantes/URL ainda devem ser preenchidos. |
| Baixa (escopo) | `src/core.py`, `src/generation.py` | Árvore SHAP e Ollama não dão diagnóstico baseado em glicemia ou HbA1c. | Manter como área técnica opcional; não depender disso na demo. |
| Baixa (PDF) | `src/lab_pdf.py` | Só PDF textual e extração sujeita a conferência. | Usar entrada manual para demo principal; PDF apenas como recurso opcional. |

## Matriz do professor
| Exigência | Evidência atual | Aceite ainda necessário |
| --- | --- | --- |
| App funcional e interface utilizável | Código, módulos, perfis sintéticos e histórico | Executar e gravar evidências em Windows |
| Persistência quando necessária | SQLite local para perfis, exames e notas | Verificar histórico local; publicar somente leitura |
| Arquitetura e documentação | `app.py`, `src`, `tests`, `README.md` | Grupo deve explicar sem copiar prompts |
| **Publicação pública** | Preparado modo de vitrine | **Não comprovada**; URL em relatório obrigatória |
| Relatório técnico 15–25 p., 22 tópicos | **19 páginas**, DOCX e PDF atualizados | Capturas atuais, nomes, referências e URL |
| Plano 5–10 p. | **8 páginas**, DOCX e PDF atualizados | Revisar viabilidade/estimativas, inserir URL |
| Pitch 15 min e 20 min de arguição | 12 slides e roteiro 3 pessoas | Ensaiar e registrar apresentação real |
| Uso de IA declarado | `docs/Uso_de_IA.md` | Conferência dos três integrantes |

### Distribuição dos 100 pontos
**Inovação/originalidade 35; relevância/impacto 20; qualidade técnica 20; viabilidade/escalabilidade 10; disseminação 10; apresentação 5.** O enunciado menciona até **−10 por ausência de publicação pública** e outras penalidades por falta de relatório, plano e declaração de IA.

## Testes observados nesta sessão
`python -m unittest discover -s tests -v`: **59 testes/módulos de descoberta**, dos quais **57 aprovaram** e **2 não iniciaram por `ModuleNotFoundError` de Streamlit/Altair**. Isso não prova sucesso dos testes Streamlit nem falha funcional nesses testes. `python -m compileall` passou para os arquivos Python. Arquivo `docs/Resultado_testes_v10.txt` registra a execução. O Git bundle foi verificado como histórico completo.

## Próximas ações sem exageros
1. Abrir `APRESENTAR_WINDOWS.bat`, verificar perfil DEMO-001, histórico e área do paciente.
2. Executar `Testar_Windows.bat` e guardar o log. Conferir os dois temas e versão móvel no navegador.
3. Publicar a vitrine somente leitura, testar o link fora do computador e comprovar ausência de formulários de escrita.
4. Registrar capturas REAIS da versão 10, substituir prévias do relatório e completar integrantes, professor, disciplina e URL.
5. Ensaiar 15 minutos, preparar resposta sobre limites médicos, IA, originalidade, dados fictícios e uso futuro.

**O que não incluir antes da banca:** chat RAG sobre prontuário real, identificação automática de diabetes tipo 2, porcentagem supostamente clínica, interoperabilidade hospitalar e autenticação de pacientes reais. Não são requisitos mínimos do enunciado e consumiriam tempo sem validação suficiente.
