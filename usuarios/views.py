from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from auditoria.utils import registrar_historial


class LoginUsuarioView(LoginView):

    template_name = "login.html"

    redirect_authenticated_user = True

    def form_valid(self, form):

        response = super().form_valid(form)

        registrar_historial(
            self.request,
            "LOGIN",
            "LOGIN",
            "Inicio de sesión en el sistema."
        )

        return response


def logout_view(request):

    registrar_historial(
        request,
        "LOGOUT",
        "LOGOUT",
        "Cierre de sesión en el sistema."
    )

    logout(request)

    return redirect("login")