import os
import shutil

def mover_archivos_origen_a_destino(origen, destino):
    """
    Mueve todos los archivos desde la carpeta de origen a la carpeta de destino.
    Elimina los archivos de la carpeta de origen después de moverlos.

    Parámetros:
    origen (str): Ruta de la carpeta de origen.
    destino (str): Ruta de la carpeta de destino.
    """
    
    # Asegurarse de que la carpeta de destino existe
    os.makedirs(destino, exist_ok=True)

    # Procesar cada archivo en la carpeta de origen
    for archivo in os.listdir(origen):
        file_path = os.path.join(origen, archivo)
        
        # Verificar si es un archivo (ignorar carpetas)
        if os.path.isfile(file_path):
            # Ruta completa del archivo en el destino
            destino_path = os.path.join(destino, archivo)
            
            # Mover el archivo a la carpeta de destino
            shutil.move(file_path, destino_path)


# Ejemplo de uso
origen = r'C:\Users\InésAlbarracín\Documents\Python\Lector Remitos\Entrada'
destino = r'C:\Users\InésAlbarracín\Documents\Python\Lector Remitos\Salida'
mover_archivos_origen_a_destino(origen, destino)
