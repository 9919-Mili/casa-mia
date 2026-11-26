from django.db import migrations

EMAILS_PERMITIDOS = [
    "annavillegas@live.com.ar",
    "milima9919@gmail.com",
]


def cargar_permitidos(apps, schema_editor):
    UsuarioPermitido = apps.get_model("tienda", "UsuarioPermitido")
    for email in EMAILS_PERMITIDOS:
        UsuarioPermitido.objects.get_or_create(email=email)


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0002_usuariopermitido_codigovalidacion"),
    ]

    operations = [
        migrations.RunPython(cargar_permitidos),
    ]