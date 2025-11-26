from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


def healthcheck(request):
    """Retorna status simples para validar deploy e integracao."""
    return JsonResponse({"status": "ok"})


@login_required
def home(request):
    """Dashboard inicial com atalhos para os modulos."""
    modules = [
        {"name": "Acidentes", "slug": "acidentes", "description": "Registros CAT e S-2210"},
        {"name": "EPI", "slug": "epi", "description": "Controle de EPIs e entregas"},
        {"name": "Exames", "slug": "exames", "description": "Gestao de exames S-2220"},
        {"name": "Inspecoes", "slug": "inspecoes", "description": "Nao conformidades e planos"},
        {"name": "Treinamentos", "slug": "treinamentos", "description": "Turmas, certificados e validade"},
        {"name": "Relatorios", "slug": "relatorios", "description": "PDFs e indicadores"},
    ]
    return render(request, "home.html", {"modules": modules})
