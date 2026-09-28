from django.http import HttpResponse


def library_home(request):
    return HttpResponse(
        "<h1>Library App</h1>"
        "<p>Welcome to the Django Library!</p>"
    )
