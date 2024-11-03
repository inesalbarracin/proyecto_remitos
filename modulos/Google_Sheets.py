import pandas as pd
import requests

# URL de la hoja publicada en formato CSV
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTaBKdM2YGJi64ZeVkNMyXDxdXNIkG08ArePdIefR4HwEIoLAks1ptTR3Xncs_27gwc9C-xI-AKvsBE/pub?gid=1769604217&single=true&output=csv'

# Nombre del archivo CSV descargado localmente
nombre_archivo_local = r'C:\Users\InésAlbarracín\Documents\Python\Lector Remitos\Excel Remitos\seguimiento_remitos.csv'


# Descargar y guardar el archivo actualizado en la ubicación especificada
def descargar_csv_desde_google_sheets(url, nombre_archivo_local):
    response = requests.get(url)
    response.raise_for_status()  # Verifica si hubo errores en la descarga
    with open(nombre_archivo_local, 'wb') as f:
        f.write(response.content)
    print(f"Archivo actualizado y guardado en {nombre_archivo_local}")

# Ejecutar la descarga
descargar_csv_desde_google_sheets(url, nombre_archivo_local)

# Cargar el CSV actualizado
df = pd.read_csv(nombre_archivo_local, header=None, names=['Numero_Remitido', 'Razon_Social'])

