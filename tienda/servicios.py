import requests
from .serializers import PaletaSerializer

URL_COLORES = "https://www.thecolorapi.com/scheme"

# Colores de la marca Casa Mía (los mismos de styles.css, sin el #)

COLORES_MARCA = [
    ("Terracota", "C96F52"),
    ("Rosa", "C98F9B"),
    ("Verde", "46544A"),
]

#Palabras clave de cada categoría (Parcial2)

PALABRAS_COMERCIAL = ["precio", "costo", "tarifa", "cuanto sale", "compra", "comprar", "asesorar"]
PALABRAS_TECNICA = ["soporte", "error", "problema", "ayuda", "devolucion"]
PALABRAS_RRHH = ["trabajo", "cv", "empleo", "linkedin", "puesto", "queja", "reclamo"]


def contiene_alguna(texto, palabras):
    # Devuelve True si el texto incluye al menos una de las palabras
    for palabra in palabras:
        if palabra in texto:
            return True
    return False


def clasificar_consulta(mensaje):
    texto = mensaje.lower()   # pasa todo a minúscula: "Precio" y "PRECIO" también cuentan

    if contiene_alguna(texto, PALABRAS_COMERCIAL):
        return "comercial"
    elif contiene_alguna(texto, PALABRAS_TECNICA):
        return "tecnica"
    elif contiene_alguna(texto, PALABRAS_RRHH):
        return "rrhh"
    else:
        return "general"


def obtener_paleta(hex_base, cantidad=5):
    # Pide a The Color API una paleta de colores que combinan con hex_base.
    # Si la API no responde, devuelve una lista vacía (el sitio sigue funcionando).
    try:
        respuesta = requests.get(URL_COLORES, params={
            "hex": hex_base,        # color de partida
            "mode": "monochrome",     # colores que combinan entre sí
            "count": cantidad,      # cuántos colores
            "format": "json",
        }, timeout=4)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except (requests.RequestException, ValueError):
        return []

    serializer = PaletaSerializer(data=datos)   # DRF valida y ordena los datos
    if not serializer.is_valid():
        return []
    return serializer.validated_data["colors"]



#API externa

def obtener_paletas():
    # Arma una paleta por cada color de la marca
    paletas = []
    for nombre, hex_base in COLORES_MARCA:
        colores = obtener_paleta(hex_base)
        if colores:
            paletas.append({
                "nombre": nombre,
                "base": "#" + hex_base,
                "colores": colores,
            })
    return paletas