from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .forms import LoginForm
from django.contrib.auth import views as auth_views

from . import views

router = DefaultRouter()
router.register(r"consultas", views.ConsultaViewSet)

app_name = "tienda"


urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("productos/", views.productos, name="productos"),
    path("ideas-para-regalar/", views.ideas_regalo, name="ideas"),
    path("nosotros/", views.nosotros, name="nosotros"),
    path("contacto/", views.contacto, name="contacto"),
    path("registro/", views.registro, name="registro"),
    path("validar-cuenta/", views.validar_cuenta, name="validar_cuenta"),
    path("login/", auth_views.LoginView.as_view(
        template_name="tienda/login.html",
        authentication_form=LoginForm,
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("panel/", views.panel, name="panel"),
    path("nuevaConsulta/", views.crear_consulta, name="crear_consulta"),
    path("modificarConsulta/<int:consulta_id>/", views.modificar_consulta, name="modificar_consulta"),
    path("eliminarConsulta/<int:consulta_id>/", views.eliminar_consulta, name="eliminar_consulta"),
    path("api/", include(router.urls)),
    path("api/paletas/", views.api_paletas, name="api_paletas"),
]



