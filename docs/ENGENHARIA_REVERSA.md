# Engenharia reversa e estudo — Esboço de pregação expositiva

## Objetivo e fluxo

Composição de esboço com evidência e aplicação por ponto. Em app.py, run valida a ficha e produz Markdown. titulo_markdown trata a forma dos títulos antes de renderizar a estrutura do esboço.

**Tecnologias identificadas** · Python.

**Revisão de referência** · `1587a985fbf8`.

## Mapa do código

| Caminho | Papel de leitura | Símbolos selecionados |
| --- | --- | --- |
| [app.py](../app.py) | Ponto de leitura para entrada ou composição | `texto`, `titulo_markdown`, `run`, `objeto_sem_campos_repetidos`, `rejeitar_constante_json`, `main` |

## Roteiro de estudo e desenvolvimento

1. Comece pelo fluxo descrito acima e localize seus pontos de entrada no mapa. Acompanhe uma entrada válida até a transformação ou a resposta.
2. Abra um teste relacionado ao fluxo e descreva qual regra ele protege. Compare o tratamento esperado para entradas válidas, inválidas e nos limites.
3. Ao adicionar uma regra, determine qual módulo controla o dado e cubra o caso nesse nível. Em seguida, confira o efeito no comando, na API ou na interface de entrada.

**Pergunta de entrevista**

Que validação preserva a relação entre um ponto, seu fundamento bíblico e a aplicação?

## Testes versionados

Arquivos para começar a leitura dos cenários de teste: [test_app.py](../test_app.py), [test_json_size_limit.py](../test_json_size_limit.py), [test_saida_markdown.py](../test_saida_markdown.py), [test_stdin.py](../test_stdin.py), [test_validation.py](../test_validation.py).

Os comandos e versões de runtime usados no CI ficam em [.github/workflows/testes.yml](../.github/workflows/testes.yml).

[Voltar ao README](../README.md).
