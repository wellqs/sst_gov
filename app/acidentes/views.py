from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ACIDENTE_STATUS_CHOICES, AcidenteForm, CATForm
from .models import Acidente


@login_required
def dashboard(request):
    """Tela inicial do modulo de acidentes/CAT com atalhos e ultimos registros."""
    stats = {
        "abertos": Acidente.objects.filter(status="ABERTO").count(),
        "analise": Acidente.objects.filter(status="EM_ANALISE").count(),
        "encerrados": Acidente.objects.filter(status="ENCERRADO").count(),
        "total": Acidente.objects.count(),
    }
    recentes = Acidente.objects.select_related("servidor", "unidade").order_by("-created_at")[:5]
    return render(request, "acidentes/index.html", {"stats": stats, "recentes": recentes})


@login_required
def acidente_list(request):
    """Listagem com filtros simples."""
    qs = Acidente.objects.select_related("servidor", "unidade", "setor").order_by("-data_ocorrencia")
    status = request.GET.get("status")
    gravidade = request.GET.get("gravidade")
    if status:
        qs = qs.filter(status=status)
    if gravidade:
        qs = qs.filter(gravidade=gravidade)
    return render(
        request,
        "acidentes/lista.html",
        {
            "acidentes": qs,
            "status_choices": ACIDENTE_STATUS_CHOICES,
            "gravidade_choices": Acidente.GRAVIDADE_CHOICES,
            "filtro_status": status or "",
            "filtro_gravidade": gravidade or "",
        },
    )


@login_required
def acidente_create(request):
    """Cria novo acidente."""
    if request.method == "POST":
        form = AcidenteForm(request.POST)
        if form.is_valid():
            acidente = form.save(commit=False)
            acidente.created_by = request.user
            acidente.save()
            messages.success(request, "Acidente registrado com sucesso.")
            return redirect("acidentes:detalhe", pk=acidente.pk)
    else:
        form = AcidenteForm(initial={"data_ocorrencia": timezone.now()})
    return render(request, "acidentes/form_acidente.html", {"form": form, "titulo": "Novo acidente"})


@login_required
def acidente_update(request, pk):
    """Edita acidente."""
    acidente = get_object_or_404(Acidente, pk=pk)
    if request.method == "POST":
        form = AcidenteForm(request.POST, instance=acidente)
        if form.is_valid():
            form.save()
            messages.success(request, "Acidente atualizado.")
            return redirect("acidentes:detalhe", pk=acidente.pk)
    else:
        form = AcidenteForm(instance=acidente)
    return render(request, "acidentes/form_acidente.html", {"form": form, "titulo": "Editar acidente"})


@login_required
def acidente_detail(request, pk):
    """Detalhe do acidente com info da CAT."""
    acidente = get_object_or_404(Acidente.objects.select_related("servidor", "unidade", "setor"), pk=pk)
    cat = getattr(acidente, "cat", None)
    return render(request, "acidentes/detalhe.html", {"acidente": acidente, "cat": cat})


@login_required
def cat_upsert(request, pk):
    """Cria ou atualiza a CAT do acidente."""
    acidente = get_object_or_404(Acidente, pk=pk)
    cat = getattr(acidente, "cat", None)
    if request.method == "POST":
        form = CATForm(request.POST, instance=cat)
        if form.is_valid():
            cat_obj = form.save(commit=False)
            cat_obj.acidente = acidente
            cat_obj.responsavel_emissao = request.user
            cat_obj.save()
            messages.success(request, "CAT salva.")
            return redirect("acidentes:detalhe", pk=acidente.pk)
    else:
        form = CATForm(instance=cat)
    return render(
        request,
        "acidentes/form_cat.html",
        {"form": form, "acidente": acidente, "titulo": "CAT do acidente"},
    )
