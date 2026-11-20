# Verificações de 20/11/2026

16 testes automatizados passaram (0,358 s nesta execução; duração varia por computador). Log em Resultado_testes.txt. Modelo real distribuído usado nos testes do núcleo e da interface. Nenhum treinamento novo.

- Núcleo: soma SHAP nos três casos, entradas inválidas, recuperação/abstenção, IDs falsos e SQLite.
- Interface AppTest: navegação, claro/escuro, recálculo ao trocar caso, bloqueio de feedback sem escolha e gravação explícita.
- Gráfico: especificação aceita pelo esquema Altair; campo contribution_pp sem pontos e escala incluindo zero, com exemplos positivos/negativos/zero.
- Conector: protocolo JSON, resposta válida, timeout, JSON inválido, ID falso, modelo não configurado e nenhum documento. HTTP simulado; não equivale a teste Ollama real.
- Estado: sucesso seguido de falha elimina rascunho do resultado exportável; falha parcial não publica partes; sem evidência não chama gerador.
- Armazenamento: rejeição de comentário inválido/longos e de payload não finito.

O teste de interface foi ajustado para submeter a escolha no mesmo ciclo do formulário (comportamento do AppTest). A suíte passou depois desse ajuste.

Não concluídos: revisão visual integral em navegador, Ollama ao vivo nesta máquina, PostgreSQL, execução Windows e hospedagem pública. Chromium local não iniciou por restrição de socket do ambiente. Testes de Streamlit não provam contraste, responsividade ou correspondência ao mockup. A geração real foi observada anteriormente nas capturas de Daniel, não nesta suíte.

Não houve consulta nova de fontes clínicas ou validação semântica/externa. A automação GitHub Actions está preparada; só executará após enviar a um repositório compatível. Não foi executada no GitHub nesta entrega.

## Auditoria independente posterior (20/11/2026)

Foi recebido o enunciado oficial (`docs/Enunciado.pdf`). As exigências e pendências estão em `docs/Matriz_requisitos.md` e `docs/Auditoria_20_11.md`. A suíte de 17 testes na sessão de auditoria teve 15 passes e 2 falhas de importação por ausência de Streamlit/Altair, não por asserções reprovadas. Ver `docs/Execucao_auditoria_local.txt`. Isso não substitui execução no Windows com Python 3.12 e dependências instaladas.
