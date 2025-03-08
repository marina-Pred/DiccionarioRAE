from rae.processor import  *
import json
import sys

class DiccionarioRAE:

    def __init__(self, palabra: str):
        if not isinstance(palabra, str):
            logging.error(f"Palabra inválida: {palabra}")
            sys.exit()
        self.palabra, self.resultado = RAEProcessor.procesar_palabra(palabra)
    
    def get_diccionario(self):
        return self.resultado
    
    def get_palabra(self):
        return self.palabra
    
    def crear_json(self):
        if self.resultado:
            with open('rae_resultados.json', 'w', encoding='utf-8') as f:
                json.dump(self.resultado, f, ensure_ascii=False, indent=4)
                logging.info(f"Archivo JSON creado con los resultados de '{self.palabra}'")
        
        logging.debug(f"No se puede crear el archivo JSON porque no hay resultados para '{self.palabra}'.")

    # Devuelve catidad de definiciones hay       
    def get_defs_count(self):
        if self.resultado=={}: return 0
        else: return len(self.resultado[self.palabra]) 
    # Devueve la definicion por indice
    def get_defs(self, idx):
        return self.resultado[self.palabra][idx]['Definicion']
    # Devuelve todas las definiciones
    def get_all_defs(self):
        res = []
        for i in self.resultado[self.palabra]:
                res.append(self.resultado[self.palabra][i]['Definicion'])
        return res
    # Devuelve todos los tipos asociados con el numero de su definicion
    def get_all_types(self):
        res = []
        for i in self.resultado[self.palabra]:
            res.append((i,self.resultado[self.palabra][i]['Tipo']))
        return res
       
    def isEmpty(self):
        if self. resultado == {}:
            return True
        return False