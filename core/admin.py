from django.contrib import admin

from .models import Cargo, Servidor, Setor, Unidade


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "sigla", "ativa")
    list_filter = ("ativa",)
    search_fields = ("nome", "sigla")


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ("nome", "unidade", "ativa")
    list_filter = ("ativa", "unidade")
    search_fields = ("nome", "unidade__nome", "unidade__sigla")


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "cbo", "ativo")
    list_filter = ("ativo",)
    search_fields = ("titulo", "cbo")


@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display = ("nome", "matricula", "cpf", "unidade", "setor", "cargo", "ativo")
    list_filter = ("ativo", "unidade", "setor", "cargo")
    search_fields = ("nome", "cpf", "matricula", "email")
    autocomplete_fields = ("usuario", "unidade", "setor", "cargo")
