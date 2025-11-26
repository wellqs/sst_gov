from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """Tela inicial do módulo de acidentes/CAT."""
    return render(request, "acidentes/index.html")
