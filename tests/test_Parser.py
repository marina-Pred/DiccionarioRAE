from bs4 import BeautifulSoup
from rae.parser import RAEParser
import pytest

SAMPLE_HTML = """
    <div class="c-definitions__item" role="definition" bis_skin_checked="1">
    <div bis_skin_checked="1"><span class="n_acep">1. </span>
    <abbr class="d" title="adjetivo">adj.</abbr> 
    <span data-id="BxLriBU|DgXmXNM">Dicho</span> 
    <span data-id="BtDkacL|BtFYznp">de</span> 
    <span data-id="b6hEWeB|b6iKApr">un</span> 
    <span data-id="9qYXXhD">color</span>: 
    <span data-id="XVv80p3|XW0u8Bu">Semejante</span>
    <span data-id="1PTvt8b">al</span> 
    <span data-id="BtDkacL|BtFYznp">de</span>
    <span data-id="ESraxkH|MiZ5vEt|NWnohQu">la</span>
    <span data-id="XCj54xx|XCjG7b8">sangre</span> 
    <span data-id="QlqTEX0|Qlr66uc|Qltkqeu">o</span>
    <span data-id="1PTvt8b">al</span> 
    <span data-id="C5sAXFD">del</span> 
    <span data-id="ZziM5kP">tomate</span>
    <span data-id="NrGK1zz|NrJCsyS">maduro</span>,
    <span data-id="c8HoARq|c8HrfrV|c8IFPyp">y</span>
    <span data-id="UkbUarn">que</span>
    <span data-id="Qu5i3z8">ocupa</span> 
    <span data-id="ESraxkH">el</span>
    <span data-id="UAqXCHh">primer</span> 
    <span data-id="NgMEY5T">lugar</span> 
    <span data-id="EuPaWdO">en</span>
    <span data-id="ESraxkH">el</span>
    <span data-id="GXFgj8a">espectro</span> 
    <span data-id="NhoAd6F">luminoso</span>.
    <abbr class="d" title="Usado también como sustantivo masculino">U. t. c. s. m.</abbr>
    </div><div class="c-definitions__item-footer" 
    bis_skin_checked="1"><div class="c-word-list" bis_skin_checked="1">
    <div class="c-word-list__label" bis_skin_checked="1"><abbr class="sin-header-inline d" title="Sinónimos o afines">Sin.:</abbr></div><ul class="c-word-list__items" role="list"><li><span><span class="sin" data-id="9qbpwWQ">colorado</span></span>, <span><span class="sin" data-id="5Nm1vcJ">bermejo</span></span>, <span><span class="sin" data-id="GBwa6TX">escarlata</span></span>, <span><span class="sin" data-id="7bAFY2A">carmesí</span></span>, <span><span class="sin" data-id="F1HNH02">encarnado</span></span>, <span><span class="sin" data-id="WnF9epr">rubro</span></span>, <span><span class="sin" data-id="JS2Nl1P">granate</span></span>, <span><span class="sin" data-id="JRTVOyU">grana<sup>2</sup></span></span>, <span><span class="sin" data-id="WjPUiaI">roso<sup>2</sup></span></span>.</li></ul></div></div></div>
    <!-- Se incluyen otras definiciones para simular el HTML completo; en las pruebas usaremos la primera -->
    <div class="c-definitions__item" role="definition">
    <div>
        <span class="n_acep">2. </span>
        <abbr class="g" title="adjetivo">adj.</abbr> 
        <span data-id="BtDkacL|BtFYznp">De</span> 
        <span data-id="9qYXXhD">color</span> 
        <span class="u">rojo.</span>
    </div>
    <div class="c-definitions__item-footer">
        <div class="c-word-list">
        <div class="c-word-list__label">
            <abbr class="sin-header-inline d" title="Sinónimos o afines">Sin.:</abbr>
        </div>
        <ul class="c-word-list__items" role="list">
            <li>
                <span><span class="sin" data-id="9qbpwWQ">colorado</span></span>, 
                <span><span class="sin" data-id="5Nm1vcJ">bermejo</span></span>, 
                <span><span class="sin" data-id="GBwa6TX">escarlata</span></span>, 
                <span><span class="sin" data-id="7bAFY2A">carmesí</span></span>, 
                <span><span class="sin" data-id="F1HNH02">encarnado</span></span>, 
                <span><span class="sin" data-id="WnF9epr">rubro</span></span>, 
                <span><span class="sin" data-id="JS2Nl1P">granate</span></span>, 
                <span><span class="sin" data-id="JRTVOyU">grana<sup>2</sup></span></span>,
                <span><span class="sin" data-id="WjPUiaI">roso<sup>2</sup></span></span>.
            </li>
        </ul>
        </div>
    </div>
    </div>
    """

class TestRAEParserConSampleHTML:

    @pytest.fixture
    def soup(self):
        return BeautifulSoup(SAMPLE_HTML, 'html.parser')
    
    @pytest.fixture
    def definicion(self):
        soup = BeautifulSoup(SAMPLE_HTML, 'html.parser')
        return soup.find('div', class_='c-definitions__item')

    def test_limpiar_definicion(self, definicion):
        resultado = RAEParser.limpiar_definicion(definicion)
        esperado = (
            "Dicho de un color : Semejante al de la sangre o al del tomate maduro, "
            "y que ocupa el primer lugar en el espectro luminoso."
        )
        assert resultado == esperado

    def test_obtener_ejemplos(self, definicion):
        ejemplos = RAEParser.obtener_ejemplos(definicion)
        assert ejemplos == []  # No hay elementos con clase 'h' en el sample

    def test_extraer_abbr(self, definicion):
        tipo, usos, sinonimos, antonimos = RAEParser.extraer_abbr(definicion)
        
        assert tipo == "adjetivo"
        assert usos == ["Usado también como sustantivo masculino"]
        assert sinonimos == [
            "colorado", "bermejo", "escarlata", "carmesí",
            "encarnado", "rubro", "granate", "grana", "roso"
        ]
        assert antonimos == []

    def test_sins_o_ants(self, definicion):
        sinonimos = RAEParser.sins_o_ants(definicion)
        assert "grana" in sinonimos  
        assert "roso" in sinonimos
        assert len(sinonimos) == 9

    def test_crear_entrada(self, definicion):
        entrada = RAEParser.crear_entrada(definicion)
        
        assert entrada == {
            'Definicion': (
                "Dicho de un color : Semejante al de la sangre o al del tomate maduro, "
                "y que ocupa el primer lugar en el espectro luminoso."
            ),
            'Tipo': "adjetivo",
            'Usos': ["Usado también como sustantivo masculino"],
            'Sinonimos': [
                "colorado", "bermejo", "escarlata", "carmesí",
                "encarnado", "rubro", "granate", "grana", "roso"
            ]
        }
        assert 'Ejemplos' not in entrada  # No hay ejemplos en el sample

    def test_obtener_definiciones_conjugaciones(self, soup):
        definiciones, conjugaciones = RAEParser.obtener_definiciones_conjugaciones(soup)
        
        # Verificar cantidad de definiciones
        assert len(definiciones) == 2, "Debería encontrar 2 definiciones"
        assert len(conjugaciones) == 0, "No debería encontrar conjugaciones en el sample"
