from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.contrib import admin


def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Сайт працює!</h1>")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
]
