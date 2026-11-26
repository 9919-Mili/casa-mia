from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import ConsultaSerializer
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import logging
import smtplib
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Consulta
from .servicios import clasificar_consulta, obtener_paletas
import secrets
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from .forms import RegistroForm, ValidarCuentaForm
from .models import UsuarioPermitido, CodigoValidacion
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Consulta, CATEGORIAS_CONSULTA
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .forms import MOTIVOS, ContactoForm

from .data import CATEGORIAS, OCASIONES, PRODUCTOS, VALORES


logger = logging.getLogger(__name__)

def inicio(request):
    destacados = [p for p in PRODUCTOS if p["destacado"]]
    return render(request, "tienda/index.html", {
        "destacados": destacados,
        "categorias": CATEGORIAS,
    })


def productos(request):
    slug = request.GET.get("categoria")
    categoria_activa = None
    for c in CATEGORIAS:
        if c["slug"] == slug:
            categoria_activa = c

    if categoria_activa:
        categorias = [categoria_activa]
    else:
        categorias = CATEGORIAS

    grupos = []
    for c in categorias:
        lista = [p for p in PRODUCTOS if p["categoria"] == c["slug"]]
        grupos.append({"categoria": c, "productos": lista})

    return render(request, "tienda/productos.html", {
        "grupos": grupos,
        "categorias": CATEGORIAS,
        "categoria_activa": categoria_activa,
    })


def ideas_regalo(request):
    ocasiones = []
    for o in OCASIONES:
        lista = [p for p in PRODUCTOS if p["id"] in o["productos"]]
        ocasiones.append({
            "titulo": o["titulo"],
            "tono": o["tono"],
            "foto": o["foto"],
            "texto": o["texto"],
            "productos": lista,
            "desde": min(p["precio"] for p in lista) if lista else None,
        })
    return render(request, "tienda/ideasregalar.html", {
        "ocasiones": ocasiones,
        "paletas": obtener_paletas(),
    })


def nosotros(request):
    return render(request, "tienda/nosotros.html", {"valores": VALORES})


def enviar_confirmacion(consulta):

    """Correo de respuesta automatica al usuario"""

    contexto = {
        "nombre": consulta.nombre,
        "email": consulta.email,
        "telefono": consulta.telefono,
        "mensaje": consulta.mensaje,
        "motivo_texto": consulta.get_motivo_display(),
        "categoria": consulta.get_categoria_display(),
        "primer_nombre": consulta.nombre.split()[0],
    }

    confirmacion = EmailMultiAlternatives(
        subject=f"[{consulta.get_categoria_display()}] Recibimos tu consulta | Casa Mía",
        body=render_to_string("tienda/email/confirmacion.txt", contexto),
        to=[consulta.email],
    )
    confirmacion.attach_alternative(
        render_to_string("tienda/email/confirmacion.html", contexto), "text/html"
    )
    confirmacion.send()


def enviar_aviso_tienda(consulta):

    """Aviso interno para la tienda con todos los datos cargados"""
    aviso = EmailMultiAlternatives(
        subject=f"[{consulta.get_categoria_display()}] Nueva consulta web de {consulta.nombre}",
        body=(
            f"Nombre: {consulta.nombre}\n"
            f"Correo: {consulta.email}\n"
            f"Teléfono: {consulta.telefono or '-'}\n"
            f"Motivo: {consulta.get_motivo_display()}\n"
            f"Categoría: {consulta.get_categoria_display()}\n\n"
            f"{consulta.mensaje}"
        ),
        to=["maraujo@proyectoweb.website"],
        reply_to=[consulta.email],
    )
    aviso.send()


def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data

            # Clasificar la consulta según el mensaje
            categoria = clasificar_consulta(datos["mensaje"])

            # Guardar en la base de datos (CREATE)
            consulta = Consulta.objects.create(**datos, categoria=categoria)

            try:
                enviar_confirmacion(consulta)
            except (smtplib.SMTPException, OSError) as error:
                # Falló el correo al usuario: esto sí es un error
                print("ERROR DE MAIL (confirmación):", repr(error))
                messages.error(
                    request,
                    "No pudimos enviarte el correo de confirmación. "
                    "Revisá que tu correo esté bien escrito o probá de nuevo en unos minutos.",
                )
            else:
                # La confirmación salió bien.  Aviso a la tienda.
                try:
                    enviar_aviso_tienda(consulta)
                except (smtplib.SMTPException, OSError) as error:
                    # Si falla, lo anotamos en la consola, pero el usuario no se entera
                    print("ERROR DE MAIL (aviso tienda):", repr(error))

                messages.success(
                    request,
                    "¡Gracias! Recibimos tu consulta, pronto enviaremos un correo de confirmación.",
                )
                return redirect("tienda:contacto")
    else:
        form = ContactoForm()
    return render(request, "tienda/contacto.html", {"form": form})

# Registro de usuarios permitidos
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data

            # 1. ¿El email está en la tabla de usuarios permitidos?
            if not UsuarioPermitido.objects.filter(email__iexact=datos["email"]).exists():
                messages.error(request, "Acceso restringido. No está autorizado a utilizar este sistema.")
                return render(request, "tienda/registro.html", {"form": form})

            # 2. Crear el usuario INACTIVO (no puede entrar hasta validar)
            usuario = User.objects.create_user(
                username=datos["email"],      # usamos el email como nombre de usuario
                email=datos["email"],
                password=datos["password1"],  # create_user la guarda encriptada
                first_name=datos["nombre"],
                last_name=datos["apellido"],
            )
            usuario.is_active = False
            usuario.save()

            # 3. Generar el código de 6 números y guardarlo
            codigo = f"{secrets.randbelow(1000000):06d}"
            CodigoValidacion.objects.create(usuario=usuario, codigo=codigo)

            # 4. Mandar el mail con el código y el enlace
            enlace = request.build_absolute_uri(reverse("tienda:validar_cuenta")) + f"?email={usuario.email}"
            try:
                send_mail(
                    "Validá tu cuenta | Casa Mía",
                    (
                        f"Hola {usuario.first_name}:\n\n"
                        f"Tu código de validación es: {codigo}\n\n"
                        f"Ingresalo en este enlace para activar tu cuenta:\n{enlace}\n\n"
                        f"El equipo de Casa Mía"
                    ),
                    None,
                    [usuario.email],
                )
            except Exception:
                logger.exception("No se pudo enviar el mail de validación")
                usuario.delete()   # si no llegó el mail, deshacemos el registro para que pueda reintentar
                messages.error(request, "No pudimos enviar el correo de validación. Probá de nuevo en unos minutos.")
                return render(request, "tienda/registro.html", {"form": form})

            messages.success(request, "Le llegará un correo para validar su cuenta.")
            return redirect(enlace)
    else:
        form = RegistroForm()
    return render(request, "tienda/registro.html", {"form": form})


# Validación de cuenta con el código recibido por mail

def validar_cuenta(request):
    if request.method == "POST":
        form = ValidarCuentaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            codigo = form.cleaned_data["codigo"]

            registro_codigo = CodigoValidacion.objects.filter(
                usuario__username=email, codigo=codigo
            ).first()

            if registro_codigo:
                usuario = registro_codigo.usuario
                usuario.is_active = True      # habilita el acceso
                usuario.save()
                registro_codigo.delete()      # el código ya no sirve más
                messages.success(request, "¡Cuenta validada! Ya podés iniciar sesión.")
                return redirect("tienda:login")

            messages.error(request, "El código o el correo no son correctos.")
    else:
        # Si viene desde el enlace del mail, el email ya queda cargado
        form = ValidarCuentaForm(initial={"email": request.GET.get("email", "")})
    return render(request, "tienda/validarcuenta.html", {"form": form})

# Panel de administración: resumen + listado (READ)
@login_required
def panel(request):
    consultas = Consulta.objects.all()

    # Resumen estadístico: cantidad por cada categoría
    resumen = []
    for clave, nombre in CATEGORIAS_CONSULTA:
        resumen.append({
            "clave": clave,
            "nombre": nombre,
            "cantidad": consultas.filter(categoria=clave).count(),
        })

    return render(request, "tienda/panel.html", {
        "consultas": consultas,
        "total": consultas.count(),
        "resumen": resumen,
    })

# Nueva consulta desde el panel (CREATE)
@login_required
def crear_consulta(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            Consulta.objects.create(**datos, categoria=clasificar_consulta(datos["mensaje"]))
            messages.success(request, "Consulta creada correctamente.")
            return redirect("tienda:panel")
    else:
        form = ContactoForm()
    return render(request, "tienda/crearConsulta.html", {"form": form})


# Modificar consulta (UPDATE)
@login_required
def modificar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    if request.method == "POST":
        form = ContactoForm(request.POST)
        if not form.is_valid():
            errores = {campo: [e["message"] for e in lista]
                       for campo, lista in form.errors.get_json_data().items()}
            return JsonResponse({"success": False, "errors": errores}, status=400)

        # Actualizar los valores de la consulta
        consulta.nombre = form.cleaned_data["nombre"]
        consulta.email = form.cleaned_data["email"]
        consulta.telefono = form.cleaned_data["telefono"]
        consulta.motivo = form.cleaned_data["motivo"]
        consulta.mensaje = form.cleaned_data["mensaje"]
        consulta.categoria = clasificar_consulta(consulta.mensaje)  # se recalcula con el mensaje nuevo
        consulta.save()

        return JsonResponse({"success": True, "message": "Consulta modificada correctamente."})

    # Llena el formulario con los datos actuales
    form = ContactoForm(initial={
        "nombre": consulta.nombre,
        "email": consulta.email,
        "telefono": consulta.telefono,
        "motivo": consulta.motivo,
        "mensaje": consulta.mensaje,
    })
    return render(request, "tienda/modificarConsulta.html", {"form": form, "consulta": consulta})


# Eliminar consulta (DELETE)
@login_required
@require_POST
def eliminar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    consulta.delete()
    return JsonResponse({"success": True, "message": "Consulta eliminada correctamente."})

# API propia: /api/consultas/
class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()              # todas las consultas de la base
    serializer_class = ConsultaSerializer          # cómo convertirlas a JSON
    permission_classes = [IsAuthenticatedOrReadOnly]  # leer cualquiera / modificar solo logueados

    # Si se crea o modifica por la API, la categoría también se calcula sola
    def perform_create(self, serializer):
        serializer.save(categoria=clasificar_consulta(serializer.validated_data["mensaje"]))

    def perform_update(self, serializer):
        mensaje = serializer.validated_data.get("mensaje", serializer.instance.mensaje)
        serializer.save(categoria=clasificar_consulta(mensaje))


# API: paletas de colores obtenidas de la API externa
@api_view(["GET"])
def api_paletas(request):
    return Response(obtener_paletas())