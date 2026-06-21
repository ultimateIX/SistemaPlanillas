from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.historial_cambios,
        name="historial_cambios"
    ),

]