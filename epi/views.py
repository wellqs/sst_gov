from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EPIForm, EntregaEPIForm
from .models import EPI, EntregaEPI


@login_required
def dashboard(request):
    """Dashboard de EPIs com alertas basicos."""
    hoje = date.today()
    limite_breve = hoje + timedelta(days=30)
    total_epi = EPI.objects.filter(ativo=True).count()
    total_entregas = EntregaEPI.objects.count()
    vencidos = EPI.objects.filter(ativo=True, validade_ca__isnull=False, validade_ca__lte=hoje).count()
    em_breve = EPI.objects.filter(
        ativo=True,
        validade_ca__isnull=False,
        validade_ca__gt=hoje,
        validade_ca__lte=limite_breve,
    ).count()

    ultimas_entregas = (
        EntregaEPI.objects.select_related("epi", "servidor")
        .order_by("-data_entrega")[:5]
    )
    return render(
        request,
        "epi/index.html",
        {
            "total_epi": total_epi,
            "total_entregas": total_entregas,
            "vencidos": vencidos,
            "em_breve": em_breve,
            "ultimas_entregas": ultimas_entregas,
        },
    )


# Catalogo de EPIs (gestao)
@login_required
def epi_list(request):
    epis = EPI.objects.all().order_by("nome")
    return render(request, "epi/epis_list.html", {"epis": epis})


@login_required
def epi_create(request):
    if request.method == "POST":
        form = EPIForm(request.POST)
        if form.is_valid():
            epi = form.save(commit=False)
            epi.created_by = request.user
            epi.save()
            messages.success(request, "EPI cadastrado.")
            return redirect("epi:catalogo")
    else:
        form = EPIForm()
    return render(request, "epi/form_epi.html", {"form": form})


@login_required
def epi_update(request, pk):
    epi = get_object_or_404(EPI, pk=pk)
    if request.method == "POST":
        form = EPIForm(request.POST, instance=epi)
        if form.is_valid():
            form.save()
            messages.success(request, "EPI atualizado.")
            return redirect("epi:catalogo")
    else:
        form = EPIForm(instance=epi)
    return render(request, "epi/form_epi.html", {"form": form})


# Entregas
@login_required
def entrega_list(request):
    """Listagem de entregas com filtro simples por status."""
    status = request.GET.get("status")
    qs = EntregaEPI.objects.select_related("epi", "servidor").order_by("-data_entrega")
    if status:
        qs = qs.filter(status=status)
    return render(
        request,
        "epi/lista.html",
        {
            "entregas": qs,
            "status": status or "",
            "status_choices": EntregaEPI.STATUS_CHOICES,
        },
    )


@login_required
def entrega_create(request):
    """Nova entrega."""
    if request.method == "POST":
        form = EntregaEPIForm(request.POST)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.created_by = request.user
            entrega.save()
            messages.success(request, "Entrega registrada.")
            return redirect("epi:entrega_detalhe", pk=entrega.pk)
    else:
        form = EntregaEPIForm()
    return render(request, "epi/form_entrega.html", {"form": form, "titulo": "Nova entrega"})


@login_required
def entrega_update(request, pk):
    """Editar entrega."""
    entrega = get_object_or_404(EntregaEPI, pk=pk)
    if request.method == "POST":
        form = EntregaEPIForm(request.POST, instance=entrega)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrega atualizada.")
            return redirect("epi:entrega_detalhe", pk=entrega.pk)
    else:
        form = EntregaEPIForm(instance=entrega)
    return render(request, "epi/form_entrega.html", {"form": form, "titulo": "Editar entrega"})


@login_required
def entrega_detail(request, pk):
    """Detalhe da entrega."""
    entrega = get_object_or_404(EntregaEPI.objects.select_related("epi", "servidor"), pk=pk)
    return render(request, "epi/detalhe.html", {"entrega": entrega})
