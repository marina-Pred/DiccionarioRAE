from unittest.mock import patch, Mock
from rae.html_handler import RAEHTMLHandler
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

def test_obtener_html_correcto():
    # Simulamos una respuesta exitosa
    with patch('urllib.request.urlopen') as mock_urlopen:  # Mockea el urlopen correcto
        # Configurar mock de respuesta
        mock_response = Mock()
        mock_response.read.return_value = b"<html>contenido</html>"  # ¡Usa bytes!
        mock_urlopen.return_value = mock_response
        
        handler = RAEHTMLHandler("rojo")
        html = handler.obtener_html()  # Debería ser un BeautifulSoup
        
        assert html is not None
        assert isinstance(html, BeautifulSoup)
        # Verifica que el HTML se parseó correctamente
        assert html.find("html") is not None

def test_obtener_html_error_urLError():
    # Simulamos un error de URL
    with patch('rae.html_handler.urlopen', side_effect=URLError("error de conexión")):
        handler = RAEHTMLHandler("rojo")
        html = handler.obtener_html()
        assert html is None

def test_obtener_html_error_HTTPError():
    # Simulamos un error HTTP
    with patch('rae.html_handler.urlopen', side_effect=HTTPError("url", 404, "Not Found", {}, None)):
        handler = RAEHTMLHandler("rojo")
        html = handler.obtener_html()
        assert html is None

def test_obtener_html_error_generico():
    # Simulamos un error genérico
    with patch('rae.html_handler.urlopen', side_effect=Exception("Error inesperado")):
        handler = RAEHTMLHandler("rojo")
        html = handler.obtener_html()
        assert html is None