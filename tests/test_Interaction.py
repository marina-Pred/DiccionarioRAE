from rae.interaction import RAEInteraccion
def test_manejar_sugerencias_valida():
    sugerencias = ["sugerencia1, extra info", "sugerencia2, extra info"]
    inputs = iter(["2"])
    input_func = lambda prompt: next(inputs)
    
    resultado = RAEInteraccion.manejar_sugerencias(sugerencias, input_func=input_func)
    assert resultado == "sugerencia2"

def test_manejar_sugerencias_salir():
    sugerencias = ["sugerencia1, extra info", "sugerencia2, extra info"]
    inputs = iter(["0"])
    input_func = lambda prompt: next(inputs)
    
    resultado = RAEInteraccion.manejar_sugerencias(sugerencias, input_func=input_func)
    assert resultado is None

def test_manejar_sugerencias_intentos_excedidos(monkeypatch):
    sugerencias = ["sugerencia1, extra info"]
    inputs = iter(["abc", "5", "x"])
    input_func = lambda prompt: next(inputs)
    
    resultado = RAEInteraccion.manejar_sugerencias(sugerencias, input_func=input_func, max_intentos=3)
    assert resultado is None