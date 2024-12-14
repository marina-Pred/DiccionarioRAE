from rae.parser  import *
from rae.html_handler import *
from rae.interaction import *

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
    def procesar_palabra(palabra):
        print(palabra)
        handler = RAEHTMLHandler(palabra)
        soup = handler.obtener_html()
            
        definiciones,conjugaciones = RAEParser.obtener_definiciones_conjugaciones(soup)
        if definiciones: 
            logging.info(f"Diccionario creado con los resultados de '{palabra}'")
            return palabra, {palabra: RAEProcessor.a_dict(definiciones, conjugaciones)}
        
        sugerencias = RAEParser.obtener_sugerencias(soup)
        if sugerencias:
             logging.warning(f""" No se encontraron definiciones para la palabra '{palabra}'. Elige una sugerencia, o pulsa 0 para salir.""")
             nueva_palabra = RAEInteraccion.manejar_sugerencias(sugerencias)
             if nueva_palabra: 
                return RAEProcessor.procesar_palabra(nueva_palabra)
                
        else:
            logging.warning(f"La palabra '{palabra}' no está en el diccionario.")
            return palabra, {}