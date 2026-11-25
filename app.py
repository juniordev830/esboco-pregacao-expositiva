'Gere um esboço em Markdown com ideia central, evidência bíblica e aplicação para cada ponto.'


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def titulo_markdown(value):
    return " ".join(parte.strip() for parte in texto(value).splitlines() if parte.strip())


def minutos(value, nome, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"{nome} deve ser um inteiro a partir de {minimo}.")
    return value


def planejar_tempo(data, pontos):
    total = minutos(data["tempo_total"], "tempo_total", 1)
    abertura = minutos(data.get("tempo_abertura", 0), "tempo_abertura")
    conclusao = minutos(data.get("tempo_conclusao", 0), "tempo_conclusao")
    agenda = []
    atual = abertura
    for ordem, ponto in enumerate(pontos, 1):
        duracao = minutos(ponto.get("minutos"), f"minutos do ponto {ordem}", 1)
        agenda.append({"ponto": ordem, "inicio": atual, "fim": atual + duracao})
        atual += duracao
    usado = atual + conclusao
    if usado > total:
        raise ValueError("O esboço excede o tempo total da pregação.")
    return {"total": total, "abertura": abertura, "conclusao": conclusao,
            "pontos": agenda, "minutos_livres": total - usado}


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    if not isinstance(data["pontos"], list) or any(not isinstance(item, dict) for item in data["pontos"]):
        raise ValueError("O campo pontos deve ser uma lista de objetos.")
    pontos = data["pontos"]
    if not pontos:
        raise ValueError("Inclua pelo menos um ponto no esboço.")
    secoes = [f"# {titulo_markdown(data['titulo'])}",
              f"**Texto-base** — {texto(data['texto_base'])}",
              f"**Ideia central** — {texto(data['ideia_central'])}"]
    for ordem, ponto in enumerate(pontos, 1):
        secoes.append(f"## {ordem}. {titulo_markdown(ponto['titulo'])}")
        secoes.append(f"{texto(ponto['referencia'])} — {texto(ponto['explicacao'])}")
        secoes.append(f"**Aplicação** — {texto(ponto['aplicacao'])}")
    secoes.extend(["## Conclusão", texto(data["conclusao"])])
    resultado = {"esboco_markdown": "\n\n".join(secoes), "quantidade_de_pontos": len(pontos)}
    if "tempo_total" in data:
        resultado["planejamento_tempo"] = planejar_tempo(data, pontos)
    return resultado


import argparse
from contextlib import nullcontext
import sys
import json
from pathlib import Path


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


MAX_JSON_BYTES = 1_000_000


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo JSON com os dados ou - para a entrada padrão")
    parser.add_argument("--markdown", action="store_true", help="Exportar o esboço de pregação em MARKDOWN")
    args = parser.parse_args()

    try:
        entrada = nullcontext(sys.stdin.buffer) if args.entrada == "-" else Path(args.entrada).open("rb")
        with entrada as source:
            raw = source.read(MAX_JSON_BYTES + 1)
        if len(raw) > MAX_JSON_BYTES:
            raise ValueError("JSON excede o limite de 1 MB.")
        data = json.loads(
            raw.decode("utf-8-sig"),
                object_pairs_hook=objeto_sem_campos_repetidos,
                parse_constant=rejeitar_constante_json,
            )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except RecursionError:
        parser.exit(2, "O JSON tem níveis de aninhamento demais.\n")
    except (KeyError, TypeError, ValueError, UnicodeError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if args.markdown:
        print(result['esboco_markdown'])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

