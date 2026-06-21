from django.shortcuts import redirect


class LoginRequiredMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        rutas_libres = [

            "/usuarios/login/",
            "/admin/",
            "/static/",

        ]

        if not request.user.is_authenticated:

            for ruta in rutas_libres:

                if request.path.startswith(ruta):

                    return self.get_response(request)

            return redirect("login")

        return self.get_response(request)