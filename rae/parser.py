from bs4 import BeautifulSoup
import re

class RAEParser:
    """Clase para extraer datos del HTML de la RAE."""

    @staticmethod
    def obtener_definiciones_conjugaciones(soup: BeautifulSoup) -> list:
        """Extrae las definiciones principales del HTML."""
        return soup.find_all('div', class_="c-definitions__item"), soup.find_all('div', class_='c-collapse')

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
        return [ej.get_text(separator=" ", strip=True) for ej in definicion.find_all('span', class_='h')]
 
    @staticmethod
    def extraer_abbr(definicion):
        tipo, usos, sinonimos, antonimos = "", [], [], []
        abbrs = definicion.find_all('abbr')
        for i, abbr in enumerate(abbrs):
            if i == 0:
                tipo = abbr.get('title', '').strip()
            elif abbr.get_text() == 'Sin.:' :
                sinonimos += RAEParser.sins_o_ants(definicion)
            elif abbr.get_text() == 'Ant.:' :
                antonimos += RAEParser.sins_o_ants(definicion)
            else:
                usos.append(abbr.get('title', '').strip())
        if 'desusado' in usos:
            return None
        
        return tipo, usos, sinonimos, antonimos
    
    @staticmethod
    def sins_o_ants(definicion) -> list:
        return [re.sub(r'\d+', '', item.get_text(strip=True)) for item in definicion.find_all('span', class_='sin')]

    
    @staticmethod   
    def crear_entrada(definicion)-> dict:
        if (elements := RAEParser.extraer_abbr(definicion)) is None:
            return None       
        tipo, usos, sinonimos, antonimos = elements
        ejemplos = RAEParser.obtener_ejemplos(definicion)
         # Crear un diccionario por cada definición con su tipo, usos, sinonimos, antonimos y ejemplos
        
        def_entry = {'Definicion': RAEParser.limpiar_definicion(definicion), 'Tipo': tipo}
        if(usos): def_entry['Usos'] = usos
        if(sinonimos): def_entry['Sinonimos'] = sinonimos
        if(antonimos): def_entry['Antonimos'] = antonimos
        if(ejemplos): def_entry['Ejemplos'] = ejemplos

        return def_entry
    @staticmethod
    def obtener_sugerencias(soup: BeautifulSoup) -> list:
        """Extrae palabras sugeridas desde enlaces con 'title="Ir a la entrada"'."""
        return [enlace.text.strip() for enlace in soup.find_all('a', attrs={'title': "Ir a la entrada"})]
    
    @staticmethod # SIN TERMINAR
    def crear_conjugaciones(conjugaciones) -> list:
        resultado={}
        # Iteramos sobre las secciones de conjugación
        for seccion in conjugaciones:
            # Buscamos el título de la sección (como "Formas no personales", "Indicativo", etc.)
            for s in seccion.find_all('table', class_ = 'c-table'):
                filas = s.find_all('tr')
                for i in range(0, len(filas), 2):
                    if i+1 < len(filas):
                        encabezados = filas[i].find_all('th')
                        valores = filas[i + 1].find_all('td')

        return resultado