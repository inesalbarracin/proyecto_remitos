import os

def renombrar_archivo(ubicacion_actual, nuevo_nombre):
    """
    Renombra un archivo en su ubicación actual.

    Parámetros:
    - ubicacion_actual (str): Ruta completa del archivo actual, incluyendo el nombre y extensión.
    - nuevo_nombre (str): Nuevo nombre que deseas darle al archivo (sin cambiar la ubicación ni la extensión).

    Retorna:
    - La ruta completa del archivo renombrado.
    """
    # Obtener la carpeta y extensión del archivo
    carpeta_actual = os.path.dirname(ubicacion_actual)
    extension = os.path.splitext(ubicacion_actual)[1]  # Conservar la extensión original
    
    # Crear la nueva ruta completa con el nuevo nombre y extensión
    nuevo_path = os.path.join(carpeta_actual, nuevo_nombre + extension)

    # Renombrar el archivo
    try:
        os.rename(ubicacion_actual, nuevo_path)
        print(f"Archivo renombrado a: {nuevo_path}")
        return nuevo_path
    except Exception as e:
        print(f"Error al renombrar el archivo: {e}")
        return None

# Ejemplo de uso
ubicacion_actual = r'C:\Users\InésAlbarracín\Documents\Python\Lector Remitos\Entrada\20241021151754437_0001.pdf'
nuevo_nombre = 'archivo_renombrado'

# Llamada a la función
renombrar_archivo(ubicacion_actual, nuevo_nombre)
