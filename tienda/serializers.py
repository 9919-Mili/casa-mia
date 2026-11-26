from rest_framework import serializers
from .models import Consulta


# Convierte objetos Consulta a JSON y JSON a Consulta

class ConsultaSerializer(serializers.ModelSerializer):
    # Además de la clave ("comercial"), devuelve el texto ("Consulta Comercial")

    categoria_texto = serializers.CharField(source="get_categoria_display", read_only=True)

    class Meta:
        model = Consulta
        fields = ["id", "nombre", "email", "telefono", "motivo", "mensaje",
                  "categoria", "categoria_texto", "fecha_creacion"]
        read_only_fields = ["categoria", "fecha_creacion"]


# --- Serializers para la API externa de colores (The Color API) ---

# Muchos datos de la API vienen como {"value"}
class ValorSerializer(serializers.Serializer):
    value = serializers.CharField()


# Un color de la paleta: su código hex y su nombre
class ColorSerializer(serializers.Serializer):
    hex = ValorSerializer()     # {"value": "#C3684B", ...}
    name = ValorSerializer()    # {"value": "Cedar Chest", ...}


# La paleta completa que devuelve la API
class PaletaSerializer(serializers.Serializer):
    mode = serializers.CharField()
    colors = ColorSerializer(many=True)   # lista de colores