from urllib.request import Request, urlopen
import urllib.parse
import re
from bs4 import BeautifulSoup
import json

class DiccionarioRAE:
    def __init__(self, palabra):
        self.palabra = palabra
        self.resultados_json = self.__de_html_a_json__(palabra) # habria que eliminar lo de palabra que fuera ()

    def __de_html_a_json__(self, palabra):
        """ Esta función accede al diccionario de la rae y extrae la información relevante, como su
        definición, tipo gramatical, uso, sinónimos, ejemplos y si es verbo sus conjugaciones.
        Si aparece en otra entrada del diccionario saltará un aviso para que se pueda consultar la nueva entrada. """
        
        if not (palabra := self.__es_palabra__(palabra)): return

        # 1º Acceso a la página web. En la variable soup se guarda el html para procesarlo
        url="https://dle.rae.es/"+urllib.parse.quote(palabra)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req).read()
        webpage = web_byte.decode('utf-8')
        soup = BeautifulSoup(webpage, 'html.parser')
        entradas = soup.find_all('div', class_='n1') # Si existen otras entradas de la palabra
        resultados_json = {} # Dicionario done guardar toda la información relevante.
        articulos = soup.find_all('article') # En la página los 'article' contienen las definiciones
        idx = 1 # Indice
        
        # Aviso por si no existe la palabra
        if not articulos: print(f"\n-- AVISO LA PALABRA '{palabra}' NO ESTÁ EN EL DICCIONARIO. --") 
        # 2º Se recorren todas las entradas que tenga disponibles la palabra
        for articulo in articulos: 
            definiciones = articulo.find_all('p', class_=['j','j1']) 
        # Cada definición contiene la información de cada significado
            for definicion in definiciones:
                delete = False # si esta en desuso la elimino
                tipo = ""
                usos = []
                sinos = []
                ants = []
                ejemps = []
                resultado = {
                    }
                """ En <abbr> está el tipo gramatical, el uso y los sinónimos.
                    1. En la primera iteración siempre estrá el tipo gramatical.
                    2. En el resto pueden aparecer los usos o los sinónimos o los antónimos, 
                    se distinguen los sinónimos y antonimos, el resto se guardan como usos. """
                # Para obtener la definición limpia, es decir sin ningún <abbr> se eliminan, cn decompose() 
                abbrs = definicion.find_all('abbr')
                for i, abbr in enumerate(abbrs):
                    if(i == 0):
                        tipo = abbr.get('title', '').strip()
                    elif abbr.get_text()=='Sin.:':
                        sinonimos_section = abbr.find_parent('td').find_next_sibling('td')
                        for sinonimo in sinonimos_section:
                            for s in sinonimo.find_all('span', class_='sin'):
                                sinos.append(re.sub(r'\d+', '', s.get_text(strip=True)))
                            sinonimo.decompose()
                    elif abbr.get_text() == 'Ant.:':
                        antonimos_section = abbr.find_parent('td').find_next_sibling('td')
                        for antonimo in antonimos_section:
                            for a in antonimo.find_all('span', class_='sin'):
                                ants.append(re.sub(r'\d+', '', a.get_text(strip=True)))
                            antonimo.decompose()
                    else:
                        usos.append(abbr.get('title', '').strip())
                        if(abbr.get('title', '').strip() == 'desusado'): delete = True
                    abbr.decompose()

                # Ejemplos del uso de la definicion
                ejemplos = definicion.find_all('span', class_='h')
                for ej in ejemplos:
                    ejemps.append(ej.get_text(separator=" ", strip=True))
                    ej.decompose()

                # Escribe espacios entre palabras
                texto_completo = definicion.get_text(separator=" ", strip=True) 
                # Elimina el número inicial
                texto_sin_numero = re.sub(r'^\d+\.\s*', '', texto_completo).strip() 
                texto_sin_numero = texto_sin_numero.replace(abbr.get_text(), '').strip()
            
                # Guardo en el diccionario resultado sus elementos
                if(not delete):
                    resultado['Definicion'] = texto_sin_numero
                    if(tipo): resultado['Tipo'] = tipo
                    if(usos): resultado['Uso'] = usos 
                    if(sinos): resultado['Sinonimos'] = sinos
                    if(ants) : resultado['Antonimos'] = ants
                    if(ejemps): resultado['Ejemplos'] = ejemps

                # 3º Guarda el resultado de cada definicion en diccionario json
                resultados_json[idx] = resultado
                idx+=1
        
        # Si es un verbo guarda la tabla de conjugaciones
        tabla_conjugacion = []
        cnj = soup.find('table', class_='cnj')
        if cnj:
            for row in cnj.find_all('tr'):  
                cols = row.find_all(['td', 'th'])
                data = []
                for col in cols:
                    if col.get('data-g', ''):
                        data.append(col.get('data-g', ''))
                    else:
                        data.append(col.get_text(strip=True))
                tabla_conjugacion.append(data)
            #for i, row in enumerate(tabla_conjugacion):
            #   print(f"Fila {i}: {row}")
    # Estructurando la conjugación
            conjugacion = {}
            # Formas no personales
            conjugacion["Formas no personales"] = {
                "Infinitivo": tabla_conjugacion[2][3],
                "Gerundio": tabla_conjugacion[2][4],
                "Infinitivo compuesto": tabla_conjugacion[4][3],
                "Gerundio compuesto": tabla_conjugacion[4][4]
            }
            # Participio
            conjugacion["Participio"] = {
                "Participio": tabla_conjugacion[6][3]
            }
            # Indicativo
            conjugacion["Indicativo"] = {}
            conjugacion["Indicativo"]["Presente"] = []
            for i in range(9, 15):  # Asumiendo que las filas de presente están entre la 5 y la 11
                conjugacion["Indicativo"]["Presente"].append({
                    "Número": tabla_conjugacion[i][0],
                    "Persona": tabla_conjugacion[i][1],
                    "Pronombres": tabla_conjugacion[i][2],
                    "Conjugación": tabla_conjugacion[i][3]
                })
            # Subjuntivo
            conjugacion["Subjuntivo"] = {}
            conjugacion["Subjuntivo"]["Presente"] = []
            for i in range(18, 25):  # Asumiendo que las filas de subjuntivo están entre la 18 y la 24
                conjugacion["Subjuntivo"]["Presente"].append({
                    "Número": tabla_conjugacion[i][0],
                    "Persona": tabla_conjugacion[i][1],
                    "Pronombres": tabla_conjugacion[i][2],
                    "Presente": tabla_conjugacion[i][3],
                    "Pretérito perfecto compuesto": tabla_conjugacion[i][4]
                })
            # Guarda las conjugaciones del verbo
            resultados_json["Conjugaciones"] = conjugacion

        # Si la palabra aprece en otras entradas, nos indica donde buscar 
        for entrada in entradas:
            otra = re.sub(r'\d+', '',entrada.find('a').get_text(strip=True))
            print(f"Existe otra entrada que contien la forma '{palabra}':  {otra}  \n")

        # Crea un archivo json
        resultados_json = {palabra: resultados_json}
        return resultados_json
    
    def __es_palabra__(self, palabra):
        try:
            cad = str(palabra) 
            # Verifica que solo contenga letras y caracteres válidos para palabras en español
            if not re.fullmatch(r"[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]+", cad):
                raise ValueError(f"La entrada '{palabra}' no es una palabra válida.")
            return cad
        except ValueError as e:
            print(e)
            return False

    def crear_json(self):
        with open('rae_resultados.json', 'w', encoding='utf-8') as f:
            json.dump(self.resultados_json, f, ensure_ascii=False, indent=4)
    # Devuelve catidad de definiciones hay       
    def get_defs_count(self):
        return len(self.resultados_json[self.palabra]) 
    # Devueve la definicion por indice
    def get_defs(self, idx):
        return self.resultados_json[self.palabra][idx]
    # Devuelve todas las definiciones
    def get_all_defs(self):
        res = []
        for i in self.resultados_json[self.palabra]:
                res.append(self.resultados_json[self.palabra][i]['Definicion'])
        return res
    # Devuelve todos los tipos asociados con el numero de su definicion
    def get_all_types(self):
        res = []
        for i in self.resultados_json[self.palabra]:
            print(self.resultados_json[self.palabra][i]['Tipo'])
            res.append((i,self.resultados_json[self.palabra][i]['Tipo']))
        return res
