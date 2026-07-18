from django.shortcuts import render
from django_phonedir.models import Department


def home_view(request):
    departments = Department.objects.order_by("name")
    return render(request, "home.html", {"departments": departments})
