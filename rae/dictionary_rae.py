from rae.parser  import *
from rae.html_handler  import *
from rae.form  import *

class DiccionarioRAE:

    def __init__(self, palabra: str):
        self.palabra = palabra
        self.resultado = self._procesar_palabra()
    
    def _procesar_palabra(self):
        handler = RAEHTMLHandler(self.palabra)
        soup = handler.obtener_html()
        if not soup:
            logging.warning(f"-- AVISO: La palabra '{self.palabra}' no está en el diccionario. --")
            return {}
        definiciones = RAEParser.obtener_definiciones(soup)
        resultado = RAEForm.a_dict(definiciones)
        return {self.palabra: resultado}
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
    