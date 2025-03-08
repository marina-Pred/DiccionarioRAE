from rae.dictionary_rae import DiccionarioRAE  

def test_diccionario_constructor():
    palabra = "casa"
    diccionario = DiccionarioRAE(palabra)

    # Verificar que la palabra se almacena correctamente
    assert diccionario.get_palabra() == palabra

    # Verificar que el resultado es un diccionario (aunque sea vacío)
    assert isinstance(diccionario.get_diccionario(), dict)

    # Verificar que no devuelve None
    assert diccionario.get_diccionario() is not None

def test_diccionario_sin_resultados():
    dict_instance = DiccionarioRAE("rossdfdsjjo")
    diccionario = dict_instance.get_diccionario()
    assert diccionario == {}

def test_diccionario_con_resultados():
    dict_instance = DiccionarioRAE("rojo")
    diccionario = dict_instance.get_diccionario()
    assert diccionario != {}

def test_crear_json():
    dict_instance = DiccionarioRAE("rojo")
    dict_instance.crear_json()
    
#######################################################################################



