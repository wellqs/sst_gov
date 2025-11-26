from django.urls import path

from . import views

app_name = "acidentes"

urlpatterns = [
    path("", views.dashboard, name="index"),
]
