from rae.parser  import *
from rae.html_handler import *
from rae.interaction import *
from typing import Tuple

METODOS = {
        "por palabras": "form",
        "por expresiones": "form2",
        "exacta": "30",
        "empieza por": "31",
        "termina en": "32",
        "contiene": "33",
        "anagramas": "anagram"
    }

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
    def procesar_palabra(palabra: str = None, metodo: str = None) -> Tuple[str, dict, list]:
        """Procesa una palabra y devuelve: palabra, resultado, sugerencias"""
        handler = RAEHTMLHandler(palabra, metodo)
        soup = handler.obtener_html()
        if not soup:
            return palabra, {}, []
        
        definiciones, conjugaciones = RAEParser.obtener_definiciones_conjugaciones(soup)
        sugerencias = RAEParser.obtener_sugerencias(soup)
        
        if metodo and not definiciones:
            return palabra, {}, sugerencias
        
        if not palabra: 
            palabra = soup.find("h1", class_="c-page-header__title").get_text().strip()
        
        if definiciones:
            return palabra, {palabra: RAEProcessor.a_dict(definiciones, conjugaciones)}, sugerencias
        
        return palabra, {}, sugerencias