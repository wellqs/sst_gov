from django.urls import path

from . import views

app_name = "epi"

urlpatterns = [
    path("", views.dashboard, name="index"),
    path("listar/", views.entrega_list, name="listar"),
    path("entrega/nova/", views.entrega_create, name="entrega_nova"),
    path("entrega/<int:pk>/", views.entrega_detail, name="entrega_detalhe"),
    path("entrega/<int:pk>/editar/", views.entrega_update, name="entrega_editar"),
    path("catalogo/", views.epi_list, name="catalogo"),
    path("catalogo/novo/", views.epi_create, name="catalogo_novo"),
    path("catalogo/<int:pk>/editar/", views.epi_update, name="catalogo_editar"),
]
