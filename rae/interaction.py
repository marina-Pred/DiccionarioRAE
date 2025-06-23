import logging
from typing import Callable, Optional
import time

class RAEInteraccion:
    """Clase para manejar la interacción con el usuario cuando hay sugerencias.
            En desuso.
        """    
    @staticmethod
    def manejar_sugerencias(sugerencias: list, input_func: Callable[[str], str] = input,
                           max_intentos: int = 3) -> Optional[str]:
        """Solicita al usuario que seleccione una sugerencia o ninguna."""
        if not sugerencias:
            return None
        opciones = "\n".join([f"{i}. {sug}" for i, sug in enumerate(sugerencias, 1)])
        mensaje = (
            f"\n Sugerencias :\n{opciones}\n"
            f"0. Salir\n"
            f"Selección [0-{len(sugerencias)}]: "
        )
        # Bucle para obtener una respuesta válida del usuario
        intentos = 0
        while intentos < max_intentos:
            try:
                seleccion = input_func(mensaje)
                if seleccion.lower() in ('q', 'quit', 'exit'):
                    logging.info("Saliendo...")
                    return None
        
                seleccion_int = int(seleccion)
                if seleccion_int == 0:
                    logging.info("Usuario seleccionó salir")
                    return None
                if 1 <= seleccion_int <= len(sugerencias):
                    seleccionada = sugerencias[seleccion_int - 1].split(",")[0].strip()
                    logging.debug(f"Sugerencia seleccionada: {seleccionada}")
                    return seleccionada

                logging.warning("Por favor, selecciona un número válido.")
                time.sleep(1)
            except ValueError:
                logging.error("Entrada inválida. Introduce un número.")
                time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Interrupción por teclado. Saliendo...")
                return None
            except Exception as e:
                logging.error(f"Error inesperado: {str(e)}")
                raise

            intentos += 1
            resto = max_intentos - intentos
            if resto > 0:
                logging.warning(f"Intentos restantes: {resto}")
                time.sleep(1)

        logging.error(f"Demasiados intentos fallidos ({max_intentos}). Saliendo...")
        return None