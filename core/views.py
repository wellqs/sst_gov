from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse


def healthcheck(request):
    """Retorna status simples para validar deploy e integracao."""
    return JsonResponse({"status": "ok"})


@login_required
def home(request):
    """Dashboard inicial com atalhos para os modulos."""
    modules = [
        {
            "name": "Acidentes",
            "slug": "acidentes",
            "description": "Registros CAT e S-2210",
            "url": reverse("acidentes:index"),
        },
        {"name": "EPI", "slug": "epi", "description": "Controle de EPIs e entregas", "url": "#epi"},
        {"name": "Exames", "slug": "exames", "description": "Gestao de exames S-2220", "url": "#exames"},
        {"name": "Inspecoes", "slug": "inspecoes", "description": "Nao conformidades e planos", "url": "#inspecoes"},
        {"name": "Treinamentos", "slug": "treinamentos", "description": "Turmas, certificados e validade", "url": "#treinamentos"},
        {"name": "Relatorios", "slug": "relatorios", "description": "PDFs e indicadores", "url": "#relatorios"},
    ]
    return render(request, "home.html", {"modules": modules})
