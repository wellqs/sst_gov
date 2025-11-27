from django.contrib import admin

from .models import EPI, EntregaEPI


@admin.register(EPI)
class EPIAdmin(admin.ModelAdmin):
    list_display = ("nome", "ca", "categoria", "tamanho", "ativo")
    list_filter = ("ativo", "categoria")
    search_fields = ("nome", "ca", "categoria")


@admin.register(EntregaEPI)
class EntregaEPIAdmin(admin.ModelAdmin):
    list_display = ("epi", "servidor", "quantidade", "data_entrega", "data_validade", "status")
    list_filter = ("status", "data_entrega")
    search_fields = ("epi__nome", "servidor__nome")
    autocomplete_fields = ("epi", "servidor")
