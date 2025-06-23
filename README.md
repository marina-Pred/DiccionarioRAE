# DiccionarioRAE

**DiccionarioRAE** es una herramienta en Python para interactuar con el Diccionario de la Real Academia Española. Permite buscar palabras en el diccionario, obtener definiciones, ejemplos, sinónimos y más.

## Instalación

1. **Instalar desde GitHub**:

   ```bash
   pip install git+https://github.com/marina-Pred/DiccionarioRAE.git

## Uso
Una vez que hayas instalado el paquete, puedes usar las funcionalidades que ofrece. A continuación, se muestran varios ejemplos de uso.

1. **Consulta básica:**

  ```python
    from rae import DiccionarioRAE

    # Crea una instancia del diccionario de una palabra aleatoria
    random = DiccionarioRAE()

    # Crear una instancia del diccionario con la palabra "llamar"
    rae = DiccionarioRAE("llamar")

    # Obtener la cantidad de definiciones para la palabra
    print(f"Cantidad de definiciones: {rae.get_defs_count()}")

2. **Consulta avanzada:**

  ```python
    from rae import DiccionarioRAE

    # Crear una instancia del diccionario con las palabras que empiecen por "roj"
    rae = DiccionarioRAE("roj","empieza por")
    print(rae.get_sugerencias())
    # Resultado de la ejecución:
    ['rojerío', 'rojear', 'rojillo', 'rojete', 'rojura', 'rojeto', 'rojo', 'rojez', 'rojigualdo', 'rojizo', 'rojal']
  ```
  **Métodos de búsqueda son:** 
  - empieza por
  - por expresiones 
  - exacta
  - termina en
  - contiene
  - anagramas

2. **Crear json:**
  ```python
    from rae import DiccionarioRAE

    rae = DiccionarioRAE("llamar")
    # Guarda en la variable "json" un string con la estructura misma que el json
    json = rae.crear_json()
    # Guarda un archivo .json en "gurdar_json" el diccionario de "llamar"
    rae.crear_json("guardar_json")
  ```
### Estructura del json
  ```json
    {
      "llamar": {
        "1": {
          "Definicion": "...",
          "Tipo": "sustantivo",
          "Sinonimos": ["..."],
          "Antonimos": ["..."],
          "Ejemplos": ["..."]
        },
        "Conjugaciones": {
          "Formas no personales": {
            "Infinitivo": "...",
            "Gerundio": "...",
            "Participio": "..."
          },
          "Indicativo": {
            "Presente": {
              "Singular": {
                "Primera": {"yo": "..."},
                "Segunda": {"tú": "..."},
                "Tercera": {"él": "..."}
              },
              "Plural": {""}
            }
          }
        }
      }
    }
  ```
## Funcionalidades

  - **Obtener la cantidad de definiciones**:
    La función **get_defs_count()** devuelve la cantidad de definiciones disponibles para la palabra buscada.

  - **Obtener todas las definiciones**:
    Utiliza **get_defs()** para obtener todas las definiciones relacionadas con la palabra.

  - **Obtener ejemplos**:
    Con **get_examples()**, puedes ver ejemplos de cómo se usa la palabra.

  - **Generar un archivo JSON**:
    **crear_json()** genera un archivo .json con la información obtenida.

## Notas

Si la palabra tiene múltiples entradas o es incorrecta, se devuelven sugerencias.
Si no se especifica palabra ni método, se consulta una palabra aleatoria.
Las conjugaciones solo se muestran si la palabra es un verbo en infinitivo.