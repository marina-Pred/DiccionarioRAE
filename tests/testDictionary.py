import unittest
from rae.dictionary_rae import DiccionarioRAE
class TestDictionary(unittest.TestCase):
    def test_buscar_palabra(self):
         # Crea una instancia del diccionario con una palabra de ejemplo
        diccionario = DiccionarioRAE('rojo')
        print(diccionario.resultado)
        self.assertIn('rojo', diccionario.resultado)  # Verificar que 'amor' está en el resultado
        # Imprime el resultado para verificar que la palabra se está procesando correctamente
