# Histórico e uso do Git

Este repositório foi criado em 20/11/2026 a partir do protótipo existente. O primeiro commit importa essa base; os seguintes registram mudanças reais feitas na revisão. Não foram inventadas datas anteriores ou autoria do grupo.

## Usar o ZIP
Extraia a pasta inteira. `.git` pode ficar oculto no explorador: não apagar. Com Git instalado, abra um terminal nessa pasta:

```sh
git log --oneline --decorate
git status
git show HEAD
```

## Restaurar pelo bundle
`Fundamento.bundle` contém o histórico completo em um único arquivo. Fora da pasta de destino, execute:

```sh
git clone Fundamento.bundle Fundamento
cd Fundamento
git log --oneline
```

Depois execute o iniciador. O bundle não contém .venv nem modelo Ollama.

## Publicar no seu próprio GitHub
Crie um repositório vazio e copie a URL real. Na raiz local:

```sh
git remote add origin URL_REAL_DO_SEU_REPOSITORIO
git push -u origin main
git push origin --tags
```

A URL é um marcador para substituir; não cole literalmente. Se já existir origin, conferir com `git remote -v` antes de alterar. Não usar force push sem entender as consequências. Nenhum repositório remoto foi criado ou publicado nesta entrega.

## Próximos commits do grupo
Configure seu nome e e-mail para os novos commits (`git config user.name` e `git config user.email`). Use alterações pequenas com motivo claro. Exemplos: `fix: corrigir contraste do seletor`, `test: cobrir resposta vazia`, `docs: incluir enunciado e matriz de requisitos`. Não usar commits vazios só para aumentar a contagem. Não reescrever autoria dos commits existentes.

O arquivo HISTORICO_COMMITS.txt acompanha a entrega para leitura sem Git.
