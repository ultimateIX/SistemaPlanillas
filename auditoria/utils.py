from .models import HistorialCambio


def registrar_historial(request, modulo, accion, descripcion):

    usuario = None

    if request.user.is_authenticated:

        usuario = request.user

    HistorialCambio.objects.create(
        usuario=usuario,
        modulo=modulo,
        accion=accion,
        descripcion=descripcion
    )