# Fundamento | Matriz de requisitos do professor

**Base:** `docs/Enunciado.pdf` (7 páginas, recebido em 20/11/2026). **Situação:** 20/11/2026, escopo ajustado para exames laboratoriais. O enunciado foi conferido, mas **a data e o horário exatos de entrega/apresentação não constam nele**. O dia 22 mencionado pelo grupo ainda requer confirmação de mês, ano e horário.

As situações abaixo distinguem a presença de código/documento de funcionamento em uma máquina real, validação pela banca e publicação na internet. Não atribuir nota presumida.

| Requisito oficial | Local do enunciado | Evidência no pacote | Situação em 20/11 | Responsável proposto | O que falta para aceitar |
|---|---|---|---|---|---|
| Originalidade, problema real, usuários e diferencial | p. 1–3 | README, módulo clínico demonstrativo e fontes SBD/ADA/NIDDK; sem entrevistas documentadas | **Parcial** | Grupo | Comparar 2–3 soluções existentes; demonstrar dor real e ganho mensurável, sem alegar produto clínico |
| Funcionalidade, interface e caso de uso | p. 3 | `app.py`, `src/clinical.py`, `src/lab_pdf.py`, casos de exames A/B/C; módulo histórico separado | **Módulo implementado por leitura; execução Streamlit no Windows pendente** | Pessoa A | Testar em Windows, temas, perfis, gráficos, gerações e erros |
| Persistência, quando necessária | p. 3 | `src/storage.py`, SQLite, testes | **Implementada localmente; hospedagem pendente** | Pessoa A | Salvar e recuperar avaliação após reinício no ambiente definitivo; não registrar pacientes |
| Arquitetura e documentação técnica | p. 3 | `README.md`, `src/`, `docs/` | **Parcial** | Pessoa A | Diagrama, requisitos e rastreabilidade em relatório acadêmico |
| **Publicação pública obrigatória** | p. 4 | Nenhuma URL pública verificável no pacote | **Não comprovada** | Pessoa A | Publicar Streamlit em host que execute Python; validar URL em outra máquina e colocar link no relatório |
| **Relatório técnico 15–25 páginas** | p. 4–5 | `docs/Entrega/Relatorio_Fundamento.docx` (19 páginas), PDF disponível | **Rascunho acadêmico produzido; revisão e evidências reais pendentes** | Pessoa C | Redigir documento com os 22 itens obrigatórios, imagens reais e referência explícita à IA |
| **Plano de disseminação 5–10 páginas** | p. 5 | `docs/Entrega/Plano_Fundamento.docx` (8 páginas), PDF disponível | **Rascunho produzido; conferência do grupo pendente** | Pessoa C | Público, canais, parceiros potenciais, adoção inicial, projeção justificada, indicadores, cronograma de 12 meses, concorrência, sustentabilidade |
| **Pitch e apresentação** | p. 5 | `docs/Entrega/Apresentacao_Fundamento.pptx`, `Roteiro_apresentacao.md` | **Slides produzidos; ensaio e demonstração real pendentes** | Grupo | Ensaiar **15 minutos de apresentação** e preparar **20 minutos de arguição**; demonstrar o app publicado |
| IA generativa declarada | p. 7 | `docs/Uso_de_IA.md`, `src/generation.py` | **Parcial** | Pessoa C | Documentar ferramentas, finalidade, trechos, alterações e avaliação crítica no relatório final |
| Testes, segurança e qualidade | p. 2 e 6 | `tests/`, logs, validação e alertas | **Parcial** | Pessoa A | Rodar suite completa no ambiente do grupo; capturar resultados, verificar proteção de dados e mobile |
| Viabilidade, escalabilidade e manutenção | p. 2, 5 e 6 | README com limitações, sem arquitetura de produção | **Parcial** | Grupo | Explicar custos, implantação, banco, geração remota, riscos e plano realista |
| Relevância e adoção no Brasil | p. 3 e 6 | Módulo laboratorial apoiado em SBD/ADA/NIDDK; modelo experimental norte-americano separado | **Lacuna relevante** | Pessoa B | Validar clinicamente a linguagem e comparar outras soluções reais sem alegar aprovação institucional |

## Partes obrigatórias do relatório técnico (15–25 páginas)

1. Resumo; 2. Introdução; 3. Problema e motivação; 4. Revisão breve de soluções existentes; 5. Público-alvo; 6. Proposta de valor; 7. Requisitos funcionais e não funcionais; 8. Arquitetura do sistema; 9. Tecnologias utilizadas; 10. Estratégia de qualidade; 11. Estratégia de segurança (quando aplicável); 12. Estratégia de testes; 13. Evidências de funcionamento; 14. Viabilidade técnica; 15. Escalabilidade; 16. Sustentabilidade tecnológica; 17. Modelo de manutenção e evolução; 18. Uso de IA generativa; 19. Limitações; 20. Trabalhos futuros; 21. Conclusões; 22. Referências.

## Plano de disseminação (5–10 páginas)

Incluir público prioritário, divulgação, canais, potenciais parceiros (não presumir parceria com Unimed), adoção inicial, projeção de usuários **identificada como hipótese**, métricas, etapas mensais em 12 meses, monetização ou sustentabilidade e comparação com concorrentes.

## Rubrica e penalidades

| Critério | Pontos |
|---|---:|
| Inovação e originalidade | 35 |
| Relevância e impacto | 20 |
| Qualidade técnica | 20 |
| Viabilidade e escalabilidade | 10 |
| Plano de disseminação | 10 |
| Apresentação e defesa | 5 |
| **Total** | **100** |

Penalidades previstas: aplicativo não funcional até -30; sem publicação -10; sem relatório -20; sem plano -10; plágio comprovado zero; IA não declarada zero. Não somar mecanicamente as penalidades como previsão de nota.

## Alteração de escopo e aceite em 20/11/2026

O projeto atual busca apresentar uma **avaliação laboratorial explicável**, não apenas SHAP de perfis históricos. Glicemia de jejum, HbA1c e TTGO são os principais exames; o sistema deve abster-se quando não há suporte. Não há probabilidade individual validada. O módulo histórico foi preservado e identificado separadamente. Foram executados testes próprios de fronteiras, contextos e PDFs; falta integração Streamlit no ambiente final. A estrutura de relatório (19 páginas), plano (8 páginas) e 12 slides foi produzida para conferência. **Link público, confirmação de integrantes, validação médica e entrega final permanecem abertos.**
