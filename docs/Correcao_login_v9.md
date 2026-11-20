# Fundamento 9 — Ajustes de tela de entrada (20/11/2026)

## Motivo

A captura da versão 8 mostrou o título `Fundamento` dividido em duas linhas (`Fundamen` + `to`) e um formulário largo alinhado à esquerda, com espaço desbalanceado na tela. A paisagem verde foi preservada.

## Mudanças

- `assets/theme.css`: define largura intrínseca e impede a quebra do título na entrada; define medidas menores para o cabeçalho e ajustes de celular.
- `app.py`: organiza o login em uma coluna central e acrescenta título e instrução curta. Mantém as mesmas credenciais fictícias e a mesma lógica de autenticação.
- Não altera perfis, exames, resultados médicos, modelo ou regras clínicas.

## Como verificar no Windows

1. Extrair o ZIP em uma pasta nova, fechar a instância anterior (confira porta 8501/8502).
2. Executar `Iniciar_Windows.bat` e abrir o endereço indicado no terminal.
3. Em 100% de zoom, testar largura grande (1920 px), intermediária (~1100 px) e estreita (~390 px).
4. Confirmar que `Fundamento` aparece em UMA linha, que a paisagem não sobrepõe os textos e que o formulário não transborda a tela.
5. Alternar Claro/Escuro; autenticar em contas paciente e médico de demonstração.
6. Rodar `Testar_Windows.bat`.

## Limites

Somente sintaxe do Python foi verificada nesta sessão; prévias HTML estáticas não substituem a execução do Streamlit no Windows. Não inserir dados reais.
