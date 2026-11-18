'Gere um esboço em Markdown com ideia central, evidência bíblica e aplicação para cada ponto.'


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def titulo_markdown(value):
    return " ".join(parte.strip() for parte in texto(value).splitlines() if parte.strip())


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
    return {"esboco_markdown": "\n\n".join(secoes), "quantidade_de_pontos": len(pontos)}


import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8") as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

