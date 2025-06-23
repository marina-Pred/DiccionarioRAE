import re
from bs4 import BeautifulSoup

from typing import Dict, List 

SELECTORS = {
    'definiciones': 'div.c-definitions__item',  
    'conjugaciones': 'div.c-collapse',
    'sugerencias': 'a[title="Ir a la entrada"]'
    }

class RAEParser:
    """Clase para extraer datos del HTML de la RAE."""

    @staticmethod
    def obtener_definiciones_conjugaciones(soup: BeautifulSoup) -> tuple:
        """Extrae las definiciones principales del HTML."""
        return (soup.select(SELECTORS['definiciones']),soup.select(SELECTORS['conjugaciones']))    
    
    @staticmethod
    def limpiar_definicion(definicion) -> str:
        # Limpia espacios y caracteres innesarios de la defincion.
        texto_completo = definicion.get_text(separator=" ", strip=True)
        texto_limpio = re.sub(r'^\d+\.\s*', '', texto_completo).strip()
        texto_limpio = re.sub(r'\s([,.\d])', r'\1', texto_limpio).strip()
        # Elimina abreviaciones, sinonimos y antonimos
        abbrs = definicion.find_all('abbr')
        sins_ants = definicion.find_all('ul')
        for abbr in abbrs:
            texto_limpio = texto_limpio.replace(abbr.get_text(), '').strip()
        for list in sins_ants: 
            texto_limpio = texto_limpio.replace(list.get_text(), '').strip()
        return texto_limpio

    @staticmethod
    def obtener_ejemplos(definicion) -> list:
        """Extrae ejemplos del texto, si están disponibles."""
        return [ej.get_text(separator=" ", strip=True) for ej in definicion.find_all('span', class_='h')]
    
    @staticmethod
    def extraer_abbr(definicion):
        """Extrae de la definicón tipo, usos, sinonimos y antonimos."""
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
        """Crear un diccionario por cada definición con su tipo, usos, sinonimos, antonimos y ejemplos"""
        if (elements := RAEParser.extraer_abbr(definicion)) is None:
            return None       
        tipo, usos, sinonimos, antonimos = elements
        ejemplos = RAEParser.obtener_ejemplos(definicion)

        def_entry = {  'Definicion': RAEParser.limpiar_definicion(definicion),'Tipo': tipo}
        if(usos): def_entry['Usos'] = usos
        if(sinonimos): def_entry['Sinonimos'] = sinonimos
        if(antonimos): def_entry['Antonimos'] = antonimos
        if(ejemplos): def_entry['Ejemplos'] = ejemplos

        return def_entry
    
    @staticmethod
    def obtener_sugerencias(soup: BeautifulSoup) -> list[str]:
        """Extrae sugerencias manteniendo solo la forma masculina cuando hay coma."""
        sugerencias = []
        
         # Caso 1: Sugerencias estándar (palabras no encontradas)
        for enlace in soup.select(SELECTORS['sugerencias']):
            texto = enlace.text.strip()
            texto = re.sub(r'\d', '', texto).strip()
            if ',' in texto:
                texto = texto.split(',')[0].strip()
            sugerencias.append(texto)
       
        # Caso 2: Redirecciones (términos compuestos)
        for header in soup.select('h3.b'):
            if header.a and 'a' in header.a.get('class', []):
                texto = header.get_text(separator=" ", strip=True)
                texto = re.sub(r'\d', '', texto).strip()
                texto = re.sub(r'\s+', ' ', texto)
                sugerencias.append(texto)
        
        return list(set(sugerencias))
    
    @staticmethod
    def crear_conjugaciones(conjugaciones) -> Dict[str, dict]:
        """Procesa tablas de conjugaciones verbales y devuelve un diccionario estructurado.
        Args:
            conjugaciones: Lista de elementos BeautifulSoup con las conjugaciones
        Returns:
            Dict: Estructura organizada por modos, tiempos, números y personas
        """
        resultado = {}
        
        for bloque in conjugaciones:
            modo = RAEParser._obtener_modo_conjugacion(bloque)
            if not modo:
                continue
                
            tablas = bloque.find_all('table')
            for tabla in tablas:
                if modo == "Formas no personales":
                    RAEParser._procesar_formas_no_personales(tabla, resultado, modo)
                else:
                    RAEParser._procesar_conjugacion_personal(tabla, resultado, modo)
                    
        return resultado

    @staticmethod
    def _obtener_modo_conjugacion(bloque) -> str:
        """Extrae el nombre del modo verbal del bloque HTML."""
        elemento_titulo = bloque.find('h3', class_='c-collapse__title')
        return elemento_titulo.get_text(strip=True) if elemento_titulo else ""

    @staticmethod
    def _procesar_formas_no_personales(tabla, resultado: dict, modo: str):
        """Procesa tablas de formas no personales (infinitivo, gerundio, participio)."""
        modo_dict = resultado.setdefault(modo, {})
        celdas_titulo = [fila.get_text() for fila in tabla.find_all('th')]
        celdas_valor = [fila.get_text() for fila in tabla.find_all('td')]
        
        for titulo, valor in zip(celdas_titulo, celdas_valor):
                modo_dict[titulo] = valor

    @staticmethod
    def _procesar_conjugacion_personal(tabla, resultado: dict, modo: str):
        """Procesa tablas de conjugaciones personales (indicativo, subjuntivo, etc.)."""
        filas = tabla.find_all('tr')
        if not filas:
            return
            
        tiempos = RAEParser._extraer_tiempos_verbales(filas[0])
        contexto = {'numero': None, 'persona': None}
        
        for fila in filas[1:]:
            contexto = RAEParser._actualizar_contexto(fila, contexto)
            pronombre, formas = RAEParser._extraer_datos_fila(fila)
            
            if not all([contexto['numero'], contexto['persona'], pronombre]):
                continue
                
            RAEParser._agregar_al_resultado(resultado, modo, tiempos, contexto, pronombre, formas)

    @staticmethod
    def _extraer_tiempos_verbales(fila_encabezado) -> List[str]:
        """Extrae los tiempos verbales de la fila de encabezado de la tabla."""
        return [th.get_text(strip=True) for th in fila_encabezado.find_all('th')[3:]]

    @staticmethod
    def _actualizar_contexto(fila, contexto_actual: dict) -> dict:
        """Actualiza el contexto de número y persona basado en las celdas de la fila."""
        nuevo_contexto = contexto_actual.copy()
        celdas_titulo = fila.find_all('th', class_='c-th-secondary')
        
        for celda in celdas_titulo:
            texto = celda.get_text(strip=True)
            if texto in ["Singular", "Plural"]:
                nuevo_contexto['numero'] = texto
            elif texto in ["Primera", "Segunda", "Tercera"]:
                nuevo_contexto['persona'] = texto
                
        return nuevo_contexto

    @staticmethod
    def _extraer_datos_fila(fila) -> tuple:
        """Extrae pronombre y formas verbales de una fila de conjugación."""
        pronombre_celda = fila.find('th', class_='c-th-secondary--visible')
        pronombre = pronombre_celda.get_text(strip=True) if pronombre_celda else None
        formas = [" ".join(td.stripped_strings) for td in fila.find_all('td')]
        return pronombre, formas

    @staticmethod
    def _agregar_al_resultado(resultado, modo: str, tiempos: list, contexto: dict, pronombre: str, formas: list):
        """Agrega las formas verbales al diccionario de resultados."""
        for indice, tiempo in enumerate(tiempos):
            if indice >= len(formas):
                continue
                
            resultado.setdefault(modo, {})\
                     .setdefault(tiempo, {})\
                     .setdefault(contexto['numero'], {})\
                     .setdefault(contexto['persona'], {})\
                     [pronombre] = formas[indice]