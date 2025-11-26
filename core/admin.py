from django.contrib import admin

from .models import Cargo, Servidor, Setor, Unidade


class AuditAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", "created_by")

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Unidade)
class UnidadeAdmin(AuditAdmin):
    list_display = ("nome", "sigla", "telefone", "ativa")
    list_filter = ("ativa", "cidade", "uf")
    search_fields = ("nome", "sigla", "cnpj", "cidade", "uf")


@admin.register(Setor)
class SetorAdmin(AuditAdmin):
    list_display = ("nome", "unidade", "codigo", "ativa")
    list_filter = ("ativa", "unidade")
    search_fields = ("nome", "unidade__nome", "unidade__sigla", "codigo")
    autocomplete_fields = ("unidade",)


@admin.register(Cargo)
class CargoAdmin(AuditAdmin):
    list_display = ("titulo", "cbo", "ativo")
    list_filter = ("ativo",)
    search_fields = ("titulo", "cbo")


@admin.register(Servidor)
class ServidorAdmin(AuditAdmin):
    list_display = ("nome", "matricula", "cpf", "unidade", "setor", "cargo", "ativo")
    list_filter = ("ativo", "unidade", "setor", "cargo")
    search_fields = ("nome", "cpf", "matricula", "email", "pis")
    autocomplete_fields = ("usuario", "unidade", "setor", "cargo")
