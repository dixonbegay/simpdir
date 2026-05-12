from django.urls import include, path

from .views import home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("", include("django_phonedir.urls")),
]
