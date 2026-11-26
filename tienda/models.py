from django.db import models
from .forms import MOTIVOS
from django.db import models
from django.contrib.auth.models import User

# Categorías que pide el parcial
CATEGORIAS_CONSULTA = [
    ("comercial", "Consulta Comercial"),
    ("tecnica", "Consulta Técnica"),
    ("rrhh", "Consulta de RRHH"),
    ("general", "Consulta General"),
]


# Tabla Consultas: guarda cada formulario de contacto

class Consulta(models.Model):
    nombre = models.CharField(max_length=60)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    motivo = models.CharField(max_length=20, choices=MOTIVOS)
    mensaje = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_CONSULTA)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'consultas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - {self.get_categoria_display()}"



# Tabla de usuarios permitidos (solo estos emails pueden registrarse)
class UsuarioPermitido(models.Model):
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'usuarios_permitidos'

    def __str__(self):
        return self.email


# Código de validación que se manda por mail al registrarse

class CodigoValidacion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'codigos_validacion'

    def __str__(self):
        return f"{self.usuario.email} - {self.codigo}"