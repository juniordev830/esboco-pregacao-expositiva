import json
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

from app import run

ROOT = Path(__file__).resolve().parent


class ProjetoTest(unittest.TestCase):
    def test_exemplo_documentado(self):
        data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        result = run(data)
        self.assertEqual(result['quantidade_de_pontos'], 2)

    def test_cli_aceita_json_utf8_com_bom(self):
        exemplo = (ROOT / "exemplo.json").read_text(encoding="utf-8")
        with TemporaryDirectory() as pasta:
            entrada = Path(pasta) / "entrada.json"
            entrada.write_text(exemplo, encoding="utf-8-sig")
            resultado = subprocess.run(
                [sys.executable, str(ROOT / "app.py"), str(entrada)],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
        self.assertEqual(json.loads(resultado.stdout), run(json.loads(exemplo)))

    def test_cli_com_exemplo(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(json.loads(result.stdout)['quantidade_de_pontos'], 2)

    def test_rejeita_dados_incompletos(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            run({})


class JsonEstritoCliTest(unittest.TestCase):
    def test_cli_rejeita_constantes_numericas_nao_padronizadas(self):
        exemplo = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        with TemporaryDirectory() as pasta:
            entrada = Path(pasta) / "entrada.json"
            for constante in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(constante=constante):
                    exemplo["metadados"] = {"observacao": "CONSTANTE_TESTE"}
                    entrada.write_text(
                        json.dumps(exemplo).replace('"CONSTANTE_TESTE"', constante),
                        encoding="utf-8",
                    )
                    resultado = subprocess.run(
                        [sys.executable, str(ROOT / "app.py"), str(entrada)],
                        capture_output=True, text=True, encoding="utf-8",
                    )
                    self.assertEqual(resultado.returncode, 2)
                    self.assertIn(constante, resultado.stderr)
                    self.assertEqual(resultado.stdout, "")

    def test_cli_rejeita_campos_json_repetidos_em_objetos_internos(self):
        exemplo = (ROOT / "exemplo.json").read_text(encoding="utf-8").rstrip()
        with TemporaryDirectory() as pasta:
            entrada = Path(pasta) / "entrada.json"
            entrada.write_text(
                exemplo[:-1] + ', "metadados": {"origem": 1, "origem": 2}}',
                encoding="utf-8",
            )
            resultado = subprocess.run(
                [sys.executable, str(ROOT / "app.py"), str(entrada)],
                capture_output=True, text=True, encoding="utf-8",
            )
        self.assertEqual(resultado.returncode, 2)
        self.assertIn("Campo JSON repetido", resultado.stderr)
        self.assertEqual(resultado.stdout, "")


class PlanejamentoTempoTest(unittest.TestCase):
    def dados(self, **extras):
        return dict(titulo="Tema", texto_base="João 15", ideia_central="Ideia",
                    conclusao="Conclusão",
                    pontos=[dict(titulo="Ponto", referencia="João 15:1",
                                 explicacao="Explicação", aplicacao="Aplicação", minutos=15)],
                    **extras)

    def test_distribui_tempo(self):
        result = run(self.dados(tempo_total=30, tempo_abertura=5, tempo_conclusao=5))
        self.assertEqual(result["planejamento_tempo"], {
            "total": 30, "abertura": 5, "conclusao": 5,
            "pontos": [{"ponto": 1, "inicio": 5, "fim": 20}],
            "minutos_livres": 5})

    def test_rejeita_excesso(self):
        with self.assertRaises(ValueError):
            run(self.dados(tempo_total=10))

    def test_rejeita_booleano(self):
        with self.assertRaises(ValueError):
            run(self.dados(tempo_total=True))

    def test_opcional(self):
        self.assertNotIn("planejamento_tempo", run(self.dados()))

    def test_rejeita_ponto_sem_duracao(self):
        dados = self.dados(tempo_total=30)
        del dados["pontos"][0]["minutos"]
        with self.assertRaises(ValueError):
            run(dados)
