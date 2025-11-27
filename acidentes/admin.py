from django.contrib import admin

from .models import CAT, Acidente


@admin.register(Acidente)
class AcidenteAdmin(admin.ModelAdmin):
    list_display = ("servidor", "tipo", "gravidade", "status", "data_ocorrencia", "unidade", "setor")
    list_filter = ("status", "gravidade", "tipo", "unidade", "setor")
    search_fields = ("servidor__nome", "descricao", "local")
    autocomplete_fields = ("servidor", "unidade", "setor")
    date_hierarchy = "data_ocorrencia"


@admin.register(CAT)
class CATAdmin(admin.ModelAdmin):
    list_display = ("numero", "acidente", "status", "data_emissao", "responsavel_emissao")
    list_filter = ("status",)
    search_fields = ("numero", "acidente__servidor__nome")
    autocomplete_fields = ("acidente", "responsavel_emissao")
