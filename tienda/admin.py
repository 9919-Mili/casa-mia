from django.contrib import admin
from .models import Consulta
from django.contrib import admin
from .models import Consulta, UsuarioPermitido, CodigoValidacion




admin.site.register(Consulta)
admin.site.register(UsuarioPermitido)
admin.site.register(CodigoValidacion)