from rae.processor import  *
import json
import sys

class DiccionarioRAE:

    def __init__(self, palabra: str = None, metodo: str = None):
        if not palabra and not metodo:
            self.palabra, self.resultado, self.sugerencias = RAEProcessor.procesar_palabra()
        elif isinstance(palabra, str):
            if not metodo:
                self.palabra, self.resultado, self.sugerencias = RAEProcessor.procesar_palabra(palabra)
            elif isinstance(metodo, str) and metodo in METODOS:
                metodo_valor = METODOS[metodo]
                self.palabra, self.resultado, self.sugerencias = RAEProcessor.procesar_palabra(palabra, metodo_valor)
            else:
                logging.error(f"Método inválido: {metodo}")
                sys.exit()
        else:
            logging.error(f"Palabra inválida: {palabra}")
            sys.exit()
                
    def get_diccionario(self):
        return self.resultado
    
    def get_palabra(self):
        return self.palabra
    
    def get_sugerencias(self):
        return self.sugerencias
    
    def crear_json(self, filename: Optional[str] = None) -> str:
        """Devuelve los resultados en formato JSON y opcionalmente los guarda en un archivo.
        Args:
            filename: Nombre del archivo a guardar (opcional)
        Returns:
            Cadena JSON con los resultados
        """
        if not self.resultado:
            logging.debug(f"No se pueden exportar resultados para '{self.palabra}' - diccionario vacío")
            return json.dumps({}) 
        
        json_data = json.dumps(self.resultado, ensure_ascii=False, indent=4)
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_data)
                logging.info(f"Archivo JSON creado: {filename} (Resultados de '{self.palabra}')")
        
        return json_data
    
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