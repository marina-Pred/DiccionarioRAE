from rae.parser  import *
from rae.html_handler  import *
from rae.form  import *
from rae.interaction import *

class DiccionarioRAE:

    def __init__(self, palabra: str):
        self.palabra = palabra
        self.resultado = self._procesar_palabra()
    
    def _procesar_palabra(self):
        handler = RAEHTMLHandler(self.palabra)
        soup = handler.obtener_html()
        definiciones = RAEParser.obtener_definiciones(soup)
        if definiciones: 
            resultado = {self.palabra: RAEForm.a_dict(definiciones)}
            return resultado
        
        sugerencias = RAEParser.obtener_sugerencias(soup)
        if sugerencias:
             logging.warning(f"No se encontraron definiciones para la palabra '{self.palabra}'.")
             nueva_palabra = RAEInteraccion.manejar_sugerencias(sugerencias)
             if nueva_palabra: 
                self.palabra = nueva_palabra
                return self._procesar_palabra()
        
        else:
            logging.warning(f"La palabra '{self.palabra}' no está en el diccionario.")
            return {}

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
    