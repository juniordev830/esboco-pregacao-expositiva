import unittest
from app import run

class TempoEsboco(unittest.TestCase):
    def data(self):
        return {"titulo":"Esperança","texto_base":"Rm 5","ideia_central":"Esperança","conclusao":"Aplicar","pontos":[{"titulo":"Ponto","referencia":"Rm 5:1","explicacao":"Explicar","aplicacao":"Aplicar","minutos":20}],"minutos_disponiveis":30,"minutos_introducao":3,"minutos_conclusao":5}
    def test_tempo(self):
        result = run(self.data())
        self.assertEqual(result["tempo"]["livres"], 2)
        self.assertIn("20 min", result["esboco_markdown"])
    def test_excede(self):
        data = self.data()
        data["minutos_disponiveis"] = 10
        with self.assertRaises(ValueError):
            run(data)
