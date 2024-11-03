import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re

# Configuración de la ruta de Tesseract si es necesario
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Función para extraer el número de remito
def extraer_numero_remito(file_path):
    """
    Extrae el número de remito de un archivo PDF o imagen, permitiendo ciertos errores comunes de OCR.
    Busca cualquier número de remito con 5 dígitos - 8 dígitos.
    """
    numero_remito = None
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Patrón flexible que permite errores comunes como 'o' en lugar de '0' y captura cualquier estructura de 5 dígitos - 8 dígitos
    patron_remito = r'[\s,]*[o0\d]{5}-[o0\d]{8}'
    
    # Procesar PDF
    if file_extension == ".pdf":
        paginas = convert_from_path(file_path, poppler_path=r'C:\Users\InésAlbarracín\Documents\Python\Release-24.08.0-0\poppler-24.08.0\Library\bin')
        for pagina in paginas:
            texto = pytesseract.image_to_string(pagina)
            remito_match = re.search(patron_remito, texto, re.IGNORECASE)
            if remito_match:
                numero_remito = remito_match.group(0).strip()  # Limpiar espacios o caracteres adicionales
                break
    
    # Procesar imágenes
    else:
        imagen = Image.open(file_path)
        texto = pytesseract.image_to_string(imagen)
        remito_match = re.search(patron_remito, texto, re.IGNORECASE)
        if remito_match:
            numero_remito = remito_match.group(0).strip()

    # Si se encontró un número de remito, limpiar errores comunes de 'o' a '0'
    if numero_remito:
        numero_remito = numero_remito.replace('o', '0').replace('O', '0')
    
    return numero_remito



# Ejemplo: Procesar todos los archivos en la carpeta de entrada
carpeta_entrada = r'C:\Users\InésAlbarracín\Documents\Python\Lector Remitos\Entrada'

# Recorrer cada archivo en la carpeta de entrada y aplicar extraer_numero_remito
for archivo in os.listdir(carpeta_entrada):
    file_path = os.path.join(carpeta_entrada, archivo)
    
    # Verificar si es un archivo PDF o imagen (ignorar carpetas)
    if os.path.isfile(file_path) and file_path.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.tif')):
        # Extraer el número de remito
        numero_remito = extraer_numero_remito(file_path)
        
        # Mostrar el resultado
        if numero_remito:
            print(f"Archivo: {archivo} - Número de Remito: {numero_remito}")
        else:
            print(f"Archivo: {archivo} - Número de Remito no encontrado.")