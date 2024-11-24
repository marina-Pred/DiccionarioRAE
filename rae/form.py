from rae.parser  import *
import json

class RAEForm:
    @staticmethod
    def a_dict(definiciones):
        """Convierte las definiciones a un formato de diccionario."""
        resultado = {}
        for i, definicion in enumerate(definiciones, 1):
            entry = RAEParser.crear_entrada(definicion)
            resultado[i] = entry
        return resultado

    @staticmethod
    def a_json(definiciones):
        """Convierte las definiciones a formato JSON."""
        return json.dumps(definiciones, ensure_ascii=False, indent=4)
