import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

MOTIVOS = [
    ("", "Elegí un motivo"),
    ("consulta", "Consulta sobre un producto"),
    ("regalo", "Ayuda para elegir un regalo"),
    ("pedido", "Pedido o Encargo especial"),
    ("Otro", "Otro"),
]


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre y Apellido",
        min_length=3,
        max_length=60,
        widget=forms.TextInput(attrs={"placeholder": "Ej: Lucía Fernández"}),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "tucorreo@ejemplo.com"}),
        error_messages={"invalid": "Ingresá un correo válido, por ejemplo nombre@dominio.com."},
    )
    telefono = forms.CharField(
        label="Teléfono (opcional)",
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "Ej: 11 5555 1234"}),
    )
    motivo = forms.ChoiceField(label="Motivo de la consulta", choices=MOTIVOS)
    mensaje = forms.CharField(
        label="Mensaje",
        min_length=10,
        max_length=800,
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "¿Qué estás buscando?…"}),
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs.setdefault("class", "input")

    # Validaciones propias: un método clean_<campo> por cada campo
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ'’ .-]+", nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre.title()

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono", "").strip()
        if telefono:
            if not re.fullmatch(r"[0-9 +()-]+", telefono):
                raise forms.ValidationError("El teléfono solo puede contener números, espacios, + ( ) y -.")
            if len(re.sub(r"\D", "", telefono)) < 8:
                raise forms.ValidationError("El teléfono debe tener al menos 8 dígitos.")
        return telefono

    def clean_motivo(self):
        motivo = self.cleaned_data["motivo"]
        if not motivo:
            raise forms.ValidationError("Elegí un motivo para poder ayudarte mejor.")
        return motivo

    # Validación que mira varios campos a la vez
    def clean(self):
        datos = super().clean()
        mensaje = datos.get("mensaje", "")
        if mensaje and len(mensaje.split()) < 3:
            self.add_error("mensaje", "Escribí al menos tres palabras para que podamos entender tu consulta.")
        return datos

class RegistroForm(forms.Form):
        nombre = forms.CharField(label="Nombre", max_length=60)
        apellido = forms.CharField(label="Apellido", max_length=60)
        email = forms.EmailField(label="Correo electrónico")
        password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
        password2 = forms.CharField(label="Repetí la contraseña", widget=forms.PasswordInput)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for campo in self.fields.values():
                campo.widget.attrs["class"] = "input"

        def clean_email(self):
            email = self.cleaned_data["email"].lower()
            if User.objects.filter(username=email).exists():
                raise forms.ValidationError("Ya existe una cuenta con este correo.")
            return email

        def clean(self):
            datos = super().clean()
            p1 = datos.get("password1")
            p2 = datos.get("password2")
            if p1 and p2 and p1 != p2:
                self.add_error("password2", "Las contraseñas no coinciden.")
            if p1:
                try:
                    validate_password(p1)  # reglas de contraseña segura de Django
                except forms.ValidationError as error:
                    self.add_error("password1", error)
            return datos

class ValidarCuentaForm(forms.Form):
        email = forms.EmailField(label="Correo electrónico")
        codigo = forms.CharField(label="Código de validación", max_length=6, min_length=6)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for campo in self.fields.values():
                campo.widget.attrs["class"] = "input"


class LoginForm(AuthenticationForm):

    # Mismo formulario de Django, pero pidiendo el correo en español
    username = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "input"

    def clean(self):
        email = self.cleaned_data.get("username", "").lower()
        self.cleaned_data["username"] = email

        # Si la cuenta existe pero todavía no fue validada, avisamos con un mensaje claro
        usuario = User.objects.filter(username=email).first()
        if usuario and not usuario.is_active and usuario.check_password(self.cleaned_data.get("password", "")):
            raise forms.ValidationError("Tu cuenta todavía no fue validada. Revisá tu correo e ingresá el código.")

        return super().clean()