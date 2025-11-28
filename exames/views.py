from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """Dashboard de exames (S-2220) com atalhos por tipo."""
    cards = [
        {
            "title": "Admissionais",
            "desc": "Registro e controle de ASO de admissão.",
            "url": "#admissionais",
        },
        {
            "title": "Periódicos",
            "desc": "Programação e vencimento de exames periódicos.",
            "url": "#periodicos",
        },
        {
            "title": "Demissionais",
            "desc": "Exames de desligamento e status de conclusão.",
            "url": "#demissionais",
        },
    ]
    return render(request, "exames/dashboard.html", {"cards": cards})
