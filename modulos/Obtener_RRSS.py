import pandas as pd

# Ruta del archivo CSV
ruta_csv = r'C:\Users\InésAlbarracín\Documents\Python\Lector Remitos\Excel Remitos\seguimiento_remitos.csv'

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv(ruta_csv, delimiter=',', names=['Folio', 'Razon_Social'], header=0)

# Función para obtener la razón social según el número de folio
def obtener_razon_social(folio, df):
    """
    Busca la razón social asociada a un número de folio.

    Parámetros:
    - folio: Número de folio (ejemplo: 1833)
    - df: DataFrame que contiene los datos del CSV

    Retorna:
    - La razón social correspondiente o None si no se encuentra.
    """
    resultado = df.loc[df["Folio"] == folio, "Razon_Social"]
    if not resultado.empty:
        return resultado.values[0]
    return None

# Ejemplo de uso
folio = 1857
razon_social = obtener_razon_social(folio, df)

if razon_social:
    print(f"Razón Social para el folio {folio}: {razon_social}")
else:
    print(f"No se encontró razón social para el folio {folio}")
