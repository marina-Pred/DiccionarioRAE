import urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import logging

RAE_BASE_URL = "https://dle.rae.es/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', handlers=[logging.StreamHandler()])
class RAEHTMLHandler:
    """Clase para manejar el HTML de la RAE."""

    def __init__(self, palabra):
        self.palabra = palabra

    def obtener_html(self) -> BeautifulSoup:
        """Obtiene el HTML de la página de la RAE para la palabra dada."""
        try:
            url=RAE_BASE_URL+urllib.parse.quote(self.palabra)
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=10) as rp: response = rp.read()
            return BeautifulSoup(response, 'html.parser')
        except HTTPError as e:
            logging.error(f"Error HTTP {e.code} - {e.reason}")
            return None
        except URLError as e:
            logging.error(f"Error de URL: {e.reason}")
            return None
        except Exception as e:
            logging.error(f"Error inesperado: {e}")
            return None