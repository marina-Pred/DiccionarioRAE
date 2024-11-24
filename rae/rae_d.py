from urllib.request import Request, urlopen
import urllib.parse
from bs4 import BeautifulSoup
import json
import logging
import re

RAE_BASE_URL = "https://dle.rae.es/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

class RAEHTMLHandler:
    """Clase para manejar el HTML de la RAE."""

    def __init__(self, palabra):
        self.palabra = palabra

    def obtener_html(self) -> BeautifulSoup:
        """Obtiene el HTML de la página de la RAE para la palabra dada."""
        try:
            url=RAE_BASE_URL+urllib.parse.quote(self.palabra)
            req = Request(url, headers=HEADERS)
            response = urlopen(req).read()#.decode('utf-8')
            return BeautifulSoup(response, 'html.parser')
        except Exception as e:
            logging.error(f"Error al obtener el HTML para '{self.palabra}': {e}")
            return None

class RAEParser:
    """Clase para extraer datos del HTML de la RAE."""

    @staticmethod
    def obtener_definiciones(soup: BeautifulSoup) -> list:
        """Extrae las definiciones principales del HTML."""
        definiciones = []
        if not soup.find('article'):
            logging.warning("No se encontraron definiciones en el HTML proporcionado.")
            return []
        articulos = soup.find_all('article')
        for articulo in articulos:
            for definicion in articulo.find_all('p', class_=['j', 'j1']):
                definiciones.append(definicion)
        return definiciones

    @staticmethod
    def limpiar_definicion(definicion) -> str:
         # Escribe espacios entre palabras
        texto_completo = definicion.get_text(separator=" ", strip=True)
        # Elimina el número inicial
        texto_limpio = re.sub(r'^\d+\.\s*', '', texto_completo).strip()
        texto_limpio = re.sub(r'\s([,.\d])', r'\1', texto_limpio).strip()
        abbrs = definicion.find_all('abbr')
        for abbr in abbrs:
            texto_limpio = texto_limpio.replace(abbr.get_text(), '').strip()
            if abbr.find_parent('td'):
                sinonimos_section = abbr.find_parent('td').find_next_sibling('td')
                for sinonimo in sinonimos_section:
                    texto_limpio = texto_limpio.replace(sinonimo.get_text(), '').strip()
        return texto_limpio

    @staticmethod
    def obtener_ejemplos(definicion):
        """Extrae ejemplos del texto, si están disponibles."""
        ejemplos = []
        for ej in definicion.find_all('span', class_='h'):
            ejemplos.append(ej.get_text(separator=" ", strip=True))
        return ejemplos
    
    @staticmethod
    def extraer_abbr(definicion):
        tipo, usos, sinonimos, antonimos = "", [], [], []
        abbrs = definicion.find_all('abbr')
        for i, abbr in enumerate(abbrs):
            if i == 0:
                tipo = abbr.get('title', '').strip()
            elif abbr.get_text() == 'Sin.:' :
                sinonimos += RAEParser.sins_o_ants(abbr)
            elif abbr.get_text() == 'Ant.:' :
                antonimos += RAEParser.sins_o_ants(abbr)
            else:
                usos.append(abbr.get('title', '').strip())
        if 'desusado' in usos:
            return None
        
        return tipo, usos, sinonimos, antonimos
    
    @staticmethod
    def sins_o_ants(abbr) -> list:
        items = []
        section = abbr.find_parent('td').find_next_sibling('td')
        for item in section.find_all('span', class_='sin'):
            items.append(re.sub(r'\d+', '', item.get_text(strip=True)))
        return items
    
    @staticmethod   
    def crear_entrada(definicion)-> dict:
        tipo, usos, sinonimos, antonimos = RAEParser.extraer_abbr(definicion)
        ejemplos = RAEParser.obtener_ejemplos(definicion)
        # Crear un diccionario por cada definición con su tipo, usos, sinonimos, antonimos y ejemplos
        def_entry = {   'Definicion': RAEParser.limpiar_definicion(definicion),
                        'Tipo': tipo,
                     }
        if(usos): def_entry['Usos'] = usos
        if(sinonimos): def_entry['Sinonimos'] = sinonimos
        if(antonimos): def_entry['Antonimos'] = antonimos
        if(ejemplos): def_entry['Ejemplos'] = ejemplos

        return def_entry
    
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
    def crear_json(self):
        with open('rae_resultados.json', 'w', encoding='utf-8') as f:
            json.dump(self.resultado, f, ensure_ascii=False, indent=4)
    # Devuelve catidad de definiciones hay       
    def get_defs_count(self):
        return len(self.resultado[self.palabra]) 
    # Devueve la definicion por indice
    def get_defs(self, idx):
        return self.resultado[self.palabra][idx]
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
diccionario = DiccionarioRAE('rojo')
diccionario.crear_json()