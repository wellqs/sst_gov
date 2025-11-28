from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.healthcheck, name="healthcheck"),
    path("gestao/", views.gestao, name="gestao"),
    path("relatorios/", views.relatorios, name="relatorios"),
    path("relatorios/saude/", views.relatorios_saude, name="relatorios_saude"),
    path("relatorios/seguranca/", views.relatorios_seguranca, name="relatorios_seguranca"),
    path("gestao/unidades/", views.unidades_list, name="gestao_unidades"),
    path("gestao/unidades/nova/", views.unidade_create, name="gestao_unidade_nova"),
    path("gestao/unidades/<int:pk>/editar/", views.unidade_update, name="gestao_unidade_editar"),
    path("gestao/setores/", views.setores_list, name="gestao_setores"),
    path("gestao/setores/novo/", views.setor_create, name="gestao_setor_novo"),
    path("gestao/setores/<int:pk>/editar/", views.setor_update, name="gestao_setor_editar"),
    path("gestao/cargos/", views.cargos_list, name="gestao_cargos"),
    path("gestao/cargos/novo/", views.cargo_create, name="gestao_cargo_novo"),
    path("gestao/cargos/<int:pk>/editar/", views.cargo_update, name="gestao_cargo_editar"),
    path("gestao/servidores/", views.servidores_list, name="gestao_servidores"),
    path("gestao/servidores/novo/", views.servidor_create, name="gestao_servidor_novo"),
    path("gestao/servidores/<int:pk>/editar/", views.servidor_update, name="gestao_servidor_editar"),
    path("api/chat/", views.chat_api, name="chat_api"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
]
