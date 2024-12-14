class RAEInteraccion:
    """Clase para manejar la interacción con el usuario cuando hay sugerencias."""
    
    @staticmethod
    def manejar_sugerencias(sugerencias: list) -> str:
        """Solicita al usuario que seleccione una sugerencia o ninguna."""
        if not sugerencias:
            return []
        for i, sugerencia in enumerate(sugerencias, start=1):
            print(f"{i}. {sugerencia}")

        # Bucle para obtener una respuesta válida del usuario
        while True:
            try:
                seleccion = int(input())
                if seleccion == 0:
                    print("No se seleccionó ninguna sugerencia. Saliendo...")
                    return []
                if 1 <= seleccion <= len(sugerencias):
                    return sugerencias[seleccion - 1]
                else:
                    print("Por favor, selecciona un número válido.")
                    continue
            except ValueError:
                print("Entrada inválida. Introduce un número.")
                continue