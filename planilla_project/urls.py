from django.contrib import admin
from django.urls import path, include

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

]