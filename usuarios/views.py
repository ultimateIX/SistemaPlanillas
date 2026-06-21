from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect


class LoginUsuarioView(LoginView):

    template_name = "login.html"

    redirect_authenticated_user = True


def logout_view(request):

    logout(request)

    return redirect("login")