from django.shortcuts import redirect


def logout_view(request):

    return redirect('/')