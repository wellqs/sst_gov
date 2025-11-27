from django.urls import path

from . import views

app_name = "acidentes"

urlpatterns = [
    path("", views.dashboard, name="index"),
    path("listar/", views.acidente_list, name="listar"),
    path("novo/", views.acidente_create, name="novo"),
    path("<int:pk>/", views.acidente_detail, name="detalhe"),
    path("<int:pk>/editar/", views.acidente_update, name="editar"),
    path("<int:pk>/cat/", views.cat_upsert, name="cat"),
]
