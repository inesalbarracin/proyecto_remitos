def limpiar_numero_remito(numero_remito):
    """
    Limpia el número de remito en el formato '00047-00001875' y lo convierte a '47-1875'.
    
    Parámetros:
    numero_remito (str): Número de remito en el formato '00047-00001875' o similar.
    
    Retorna:
    str: Número de remito en el formato '47-1875'.
    """
    # Separar en dos partes usando el guion
    parte1, parte2 = numero_remito.split('-')
    
    # Obtener el valor principal en parte1 ('47' o '52')
    if '47' in parte1:
        parte1 = '47'
    elif '52' in parte1:
        parte1 = '52'
    
    # Convertir parte2 a entero y luego a string para eliminar ceros a la izquierda
    parte2 = str(int(parte2))
    
    # Concatenar el resultado
    return f"{parte1}-{parte2}"

# Ejemplos de uso
print(limpiar_numero_remito("00047-00001875"))  # Output: 47-1875
print(limpiar_numero_remito(",00647-00001838"))  # Output: 47-1838
