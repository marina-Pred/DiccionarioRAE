# DiccionarioRAE

**DiccionarioRAE** es una herramienta en Python para interactuar con el Diccionario de la Real Academia Española. Permite buscar palabras en el diccionario, obtener definiciones, ejemplos, sinónimos y más.

## Instalación

1. **Instalar desde GitHub**:

   ```bash
   pip install git+https://github.com/marina-Pred/DiccionarioRAE.git

## Uso
Una vez que hayas instalado el paquete, puedes usar las funcionalidades que ofrece. A continuación, te muestro un ejemplo de cómo utilizarlo.

### Ejemplo de uso

	```python
	from rae import DiccionarioRAE

	# Crear una instancia del diccionario con una palabra
	rae = DiccionarioRAE("llamar")

	# Obtener la cantidad de definiciones para la palabra
	print("Cantidad de definiciones:", rae.get_defs_count())

**Funcionalidades**:

  - **Obtener la cantidad de definiciones**:
    La función **get_defs_count()** devuelve la cantidad de definiciones disponibles para la palabra buscada.

  - **Obtener todas las definiciones**:
    Utiliza **get_defs()** para obtener todas las definiciones relacionadas con la palabra.

  - **Obtener ejemplos**:
    Con **get_examples()**, puedes ver ejemplos de cómo se usa la palabra.

  - **Generar un archivo JSON**:
    **crear_json()** genera un archivo .json con la información obtenida.
