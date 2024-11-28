from bs4 import BeautifulSoup
import logging
import re

class RAEParser:
    """Clase para extraer datos del HTML de la RAE."""

    @staticmethod
    def obtener_definiciones(soup: BeautifulSoup) -> list:
        """Extrae las definiciones principales del HTML."""
        definiciones = []
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
    