from rae.parser  import *
from rae.html_handler import *
from rae.interaction import *
from typing import Tuple

class RAEProcessor:
    @staticmethod
    def a_dict(definiciones,conjugaciones):
        """Convierte las definiciones a un formato de diccionario."""
        resultado = {}
        for i, definicion in enumerate(definiciones, 1):
            entry = RAEParser.crear_entrada(definicion)
            if entry != None :resultado[i] = entry
        entry_conj = RAEParser.crear_conjugaciones(conjugaciones)
        if entry_conj:
            resultado['Conjugaciones'] = entry_conj
        return resultado

    @staticmethod
    def procesar_palabra(palabra: str, intentos_restantes: int = 3) -> Tuple[str, dict]:
        while intentos_restantes > 0:
            handler = RAEHTMLHandler(palabra)
            soup = handler.obtener_html()
            if not soup:
                intentos_restantes -= 1
                continue
            definiciones, conjugaciones = RAEParser.obtener_definiciones_conjugaciones(soup)

            if definiciones:
                return palabra, {palabra: RAEProcessor.a_dict(definiciones, conjugaciones)}
            sugerencias = RAEParser.obtener_sugerencias(soup)
            
            if not sugerencias:
                logging.warning(f"La palabra '{palabra}' no está en el diccionario.")
                return palabra, {}
            nueva_palabra = RAEInteraccion.manejar_sugerencias(sugerencias)
            
            if not nueva_palabra:
                return palabra, {}
            palabra = nueva_palabra  
            intentos_restantes -= 1
        return palabra, {}