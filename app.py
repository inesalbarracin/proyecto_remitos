import streamlit as st
import pandas as pd
import os
import shutil
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re
from modulos.Lector_Numero_Remito import extraer_numero_remito
from modulos.Limpiar_Nro_Remito import limpiar_numero_remito
from modulos.Obtener_RRSS import obtener_razon_social
from modulos.Rename_File import renombrar_archivo

# Configuración de Streamlit
st.set_page_config(page_title="Procesador de Remitos", layout="centered")

# Autenticación simple
PASSWORD = "tu_contraseña_secreta"

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if not st.session_state.password_correct:
        password = st.text_input("Ingrese la contraseña:", type="password")
        if password == PASSWORD:
            st.session_state.password_correct = True
            st.success("Acceso concedido.")
        else:
            st.error("Contraseña incorrecta.")

    return st.session_state.password_correct

# Configurar variables
UPLOAD_FOLDER = 'temp_entrada'
OUTPUT_FOLDER = 'temp_salida'
CSV_PATH = 'seguimiento_remitos.csv'
poppler_path = '/app/poppler/bin'  # Ruta de poppler en Streamlit Cloud si es necesario

# Cargar CSV
df = pd.read_csv(CSV_PATH, delimiter=',', names=['Folio', 'Razon_Social'], header=0)

# Crear carpetas temporales si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Función para procesar archivos
def procesar_archivo(file):
    file_path = os.path.join(UPLOAD_FOLDER, file.name)
    with open(file_path, "wb") as f:
        f.write(file.read())

    numero_remito = extraer_numero_remito(file_path)
    archivo_movido = False

    if numero_remito:
        numero_remito_limpio = limpiar_numero_remito(numero_remito)
        folio = numero_remito_limpio.split('-')[1]
        razon_social = obtener_razon_social(int(folio), df)
        
        if razon_social:
            nuevo_nombre = f"{numero_remito_limpio}.{razon_social}"
        else:
            nuevo_nombre = "00.REVISAR"
        
        nuevo_path = renombrar_archivo(file_path, nuevo_nombre)
        if nuevo_path:
            destino_path = os.path.join(OUTPUT_FOLDER, os.path.basename(nuevo_path))
            shutil.move(nuevo_path, destino_path)
            archivo_movido = True

    if not archivo_movido:
        destino_path = os.path.join(OUTPUT_FOLDER, f"00.REVISAR_{file.name}")
        shutil.move(file_path, destino_path)

    return destino_path

# Interfaz de carga de archivos
if check_password():
    st.title("Subir archivos de remitos")

    archivos = st.file_uploader("Cargar archivos PDF o imagen", accept_multiple_files=True, type=["pdf", "jpg", "png"])

    if archivos:
        st.write("Procesando archivos...")
        for archivo in archivos:
            destino = procesar_archivo(archivo)
            st.write(f"Archivo procesado y movido a: {os.path.basename(destino)}")

        st.success("Todos los archivos fueron procesados correctamente.")
        st.download_button(
            label="Descargar archivos procesados",
            data=open(destino, "rb").read(),
            file_name=os.path.basename(destino),
            mime="application/octet-stream"
        )
