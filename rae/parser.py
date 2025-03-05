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
    
    @staticmethod
    def crear_conjugaciones(conjugaciones) -> dict:
        """Procesa las conjugaciones verbales."""
        resultado = {
            "Formas no personales": {},
            "Indicativo": {},
            "Subjuntivo": {},
            "Imperativo": {}
        }

        def formas_no_personales(table, modo):
            """Procesa una tabla de formas no personales."""
            for row in table.find_all('tr'):
                th_cells = [th.get_text(strip=True) for th in row.find_all('th')]
                td_cells = [td.get_text(strip=True) for td in row.find_all('td')]
                for th, td in zip(th_cells, td_cells):
                    resultado[modo][th] = td

        def formas_personales(table, modo):
            """Procesa una tabla de conjugaciones para modos personales."""
            rows = table.find_all('tr')
            if not rows: return

            tiempos = [th.get_text(strip=True) for th in rows[0].find_all('th')[3:]]
            current_numero = None
            numero_span = 0
            current_persona = None
            persona_span = 0

            for row in rows[1:]:
                ths = row.find_all('th', class_='c-th-secondary')
                pronombre_el = row.find('th', class_='c-th-secondary--visible')
                pronombre = pronombre_el.get_text(strip=True) if pronombre_el else None
                conjuga = [" ".join(td.stripped_strings) for td in row.find_all('td')]

                for th in ths:
                    text = th.get_text(strip=True)
                    if text in ["Singular", "Plural"]:
                        current_numero = text
                        numero_span = int(th.get('rowspan', 1)) - 1
                        break
                else:
                    current_numero = numero_span > 0 and current_numero or None
                    numero_span = numero_span - 1 if numero_span > 0 else 0

                for th in ths:
                    text = th.get_text(strip=True)
                    if text in ["Primera", "Segunda", "Tercera"]:
                        current_persona = text
                        persona_span = int(th.get('rowspan', 1)) - 1
                        break
                else:
                    current_persona = persona_span > 0 and current_persona or None
                    persona_span = persona_span - 1 if persona_span > 0 else 0
                # Añadir al resultado 
                if current_numero and current_persona and pronombre:
                    for i, tiempo in enumerate(tiempos):
                        if i < len(conjuga):
                            resultado[modo].setdefault(tiempo, {})\
                                            .setdefault(current_numero, {})\
                                            .setdefault(current_persona, {})[pronombre] = conjuga[i]
        # Bucle para procesar cada bloque de conjugaciones
        for conj_block in conjugaciones:
            modo_el = conj_block.find('h3', class_='c-collapse__title')
            if not modo_el:
                continue
            modo = modo_el.get_text(strip=True)
            if modo == "Formas no personales":
                for table in conj_block.find_all('table'):
                    formas_no_personales(table, modo)
            else:
                for table in conj_block.find_all('table'):
                    formas_personales(table, modo)
        return resultado