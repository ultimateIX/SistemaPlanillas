from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('dashboard.urls')
    ),

    path(
        'empleados/',
        include('empleados.urls')
    ),

    path(
        'planillas/',
        include('planillas.urls')
    ),

    path(
        'usuarios/',
        include('usuarios.urls')
    ),
    path(
    "inventario/",
    include("inventario.urls")
),
path(
    "ausencias/",
    include("ausencias.urls")
),
path(
    "asistencias/",
    include("asistencias.urls")
),
path(
    "auditoria/",
    include("auditoria.urls")
),

]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)