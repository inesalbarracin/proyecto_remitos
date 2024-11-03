import streamlit as st
import pandas as pd
import requests
from io import StringIO
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re
import os
import shutil

# URL del Google Sheet publicado en formato CSV
google_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTaBKdM2YGJi64ZeVkNMyXDxdXNIkG08ArePdIefR4HwEIoLAks1ptTR3Xncs_27gwc9C-xI-AKvsBE/pub?gid=1769604217&single=true&output=csv"

# Función para cargar los datos del Google Sheet en un DataFrame
def cargar_datos_google_sheet(url):
    response = requests.get(url)
    response.raise_for_status()  # Lanza una excepción si falla la descarga
    data = StringIO(response.text)
    df = pd.read_csv(data)
    return df

# Cargar el archivo CSV desde Google Sheets
df = cargar_datos_google_sheet(google_sheet_url)

# Función para extraer el número de remito
def extraer_numero_remito(file_path):
    numero_remito = None
    file_extension = os.path.splitext(file_path)[1].lower()
    patron_remito = r'[^\d]*([o0]*47|52)-[o0]*(\d{4,5})'

    if file_extension == ".pdf":
        paginas = convert_from_path(file_path, poppler_path='/app/poppler/bin')  # Ajusta el poppler_path si es necesario
        for pagina in paginas:
            texto = pytesseract.image_to_string(pagina)
            remito_match = re.search(patron_remito, texto, re.IGNORECASE)
            if remito_match:
                parte1, parte2 = remito_match.groups()
                numero_remito = f"{parte1}-{parte2}"
                break
    else:
        imagen = Image.open(file_path)
        texto = pytesseract.image_to_string(imagen)
        remito_match = re.search(patron_remito, texto, re.IGNORECASE)
        if remito_match:
            parte1, parte2 = remito_match.groups()
            numero_remito = f"{parte1}-{parte2}"

    return numero_remito

# Función para limpiar el número de remito
def limpiar_numero_remito(numero_remito):
    parte1, parte2 = numero_remito.split('-')
    if '47' in parte1:
        parte1 = '47'
    elif '52' in parte1:
        parte1 = '52'
    parte2 = str(int(parte2))
    return f"{parte1}-{parte2}"

# Función para obtener la razón social usando el folio
def obtener_razon_social(folio, df):
    resultado = df.loc[df["Folio"] == folio, "Razon_Social"]
    if not resultado.empty:
        return resultado.values[0]
    return None

# Interfaz de usuario en Streamlit
st.title("Subir archivos de remitos")
archivos = st.file_uploader("Cargar archivos PDF o imagen", accept_multiple_files=True, type=["pdf", "jpg", "png"])

if archivos:
    st.write("Procesando archivos...")
    for archivo in archivos:
        # Guardar temporalmente el archivo en el servidor
        with open(archivo.name, "wb") as f:
            f.write(archivo.getbuffer())

        # Procesar el archivo
        numero_remito = extraer_numero_remito(archivo.name)
        archivo_movido = False

        if numero_remito:
            numero_remito_limpio = limpiar_numero_remito(numero_remito)
            folio = numero_remito_limpio.split('-')[1]
            razon_social = obtener_razon_social(int(folio), df)

            if razon_social:
                nuevo_nombre = f"{numero_remito_limpio}.{razon_social}"
            else:
                nuevo_nombre = "00.REVISAR"

            # Renombrar el archivo y moverlo a una carpeta temporal
            nuevo_path = os.path.join("temp_salida", nuevo_nombre + os.path.splitext(archivo.name)[1])
            shutil.move(archivo.name, nuevo_path)
            archivo_movido = True

        if not archivo_movido:
            destino_path = os.path.join("temp_salida", f"00.REVISAR_{archivo.name}")
            shutil.move(archivo.name, destino_path)

        st.write(f"Archivo procesado: {nuevo_nombre}")
    
    st.success("Todos los archivos fueron procesados correctamente.")
