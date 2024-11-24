import urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import logging

RAE_BASE_URL = "https://dle.rae.es/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}


class RAEHTMLHandler:
    """Clase para manejar el HTML de la RAE."""

    def __init__(self, palabra):
        self.palabra = palabra

    def obtener_html(self) -> BeautifulSoup:
        """Obtiene el HTML de la página de la RAE para la palabra dada."""
        try:
            url=RAE_BASE_URL+urllib.parse.quote(self.palabra)
            req = Request(url, headers=HEADERS)
            response = urlopen(req).read()#.decode('utf-8')
            return BeautifulSoup(response, 'html.parser')
        except Exception as e:
            logging.error(f"Error al obtener el HTML para '{self.palabra}': {e}")
            return None