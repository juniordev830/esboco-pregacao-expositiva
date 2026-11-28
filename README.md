# Esboço de pregação expositiva

**Navegação** · [Rodar](#rodar) · [Uso](#uso) · [Fontes e exemplos](#fontes-e-exemplos) · [Código e estudo](docs/ENGENHARIA_REVERSA.md)

Gere um esboço em Markdown com ideia central, evidência bíblica e aplicação para cada ponto.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Preencha um título, texto-base, ideia central e conclusão. Cada ponto do esboço requer referência, explicação e aplicação. Copie o campo `esboco_markdown` para o seu editor.

## Fontes e exemplos

Os exemplos incluem referências bíblicas, perguntas e anotações de demonstração. Consulte o texto e o contexto em uma [tradução publicada pela Sociedade Bíblica do Brasil](https://www.sbb.org.br/traducoes-da-biblia). Para aprofundar, o catálogo da [Nova Bíblia de Estudo Almeida](https://www.sbb.org.br/nova-almeida/biblias-de-estudo/biblia-de-estudo-almeida) e o do [Comentário Bíblico Pentecostal do Novo Testamento, CPAD](https://www.cpad.com.br/comentario-biblico-pentecostal-novo-testamento-/p) ajudam a identificar edições. Registre as páginas verificadas na sua própria consulta.

## Exportação para notas

Use `python app.py exemplo.json --markdown > relatorio.md` para exportar o esboço de pregação. O arquivo pode ser aberto diretamente no Obsidian ou em outro editor Markdown. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```

## Código e roteiro de estudo

Que validação preserva a relação entre um ponto, seu fundamento bíblico e a aplicação? O [guia de engenharia reversa](docs/ENGENHARIA_REVERSA.md) reúne o mapa dos módulos e uma pergunta técnica baseada no projeto.

Mantido por [João Junior](https://github.com/juniordev830).
