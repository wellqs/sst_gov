import json
import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from openai import OpenAI

from .forms import CargoForm, ServidorForm, SetorForm, UnidadeForm
from .models import Cargo, Servidor, Setor, Unidade


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
        {
            "name": "Gestao",
            "slug": "gestao",
            "description": "Cadastros de servidores, EPIs, unidades e setores",
            "url": reverse("gestao"),
        },
        {"name": "EPI", "slug": "epi", "description": "Controle de EPIs e entregas", "url": reverse("epi:index")},
        {"name": "Exames", "slug": "exames", "description": "Gestao de exames S-2220", "url": "#exames"},
        {"name": "Inspecoes", "slug": "inspecoes", "description": "Nao conformidades e planos", "url": "#inspecoes"},
        {"name": "Treinamentos", "slug": "treinamentos", "description": "Turmas, certificados e validade", "url": "#treinamentos"},
        {"name": "Relatorios", "slug": "relatorios", "description": "PDFs e indicadores", "url": "#relatorios"},
    ]
    return render(request, "home.html", {"modules": modules})


@login_required
def gestao(request):
    """Landing de gestao com atalhos para cadastros basicos."""
    cards = [
        {"title": "Servidores", "desc": "Cadastro completo de servidores", "url": reverse("gestao_servidores")},
        {"title": "Unidades", "desc": "Cadastro de unidades/secretarias", "url": reverse("gestao_unidades")},
        {"title": "Setores", "desc": "Cadastro de setores por unidade", "url": reverse("gestao_setores")},
        {"title": "Cargos", "desc": "Cadastro de cargos e CBO", "url": reverse("gestao_cargos")},
        {"title": "EPIs", "desc": "Catalogo de EPIs e CAs", "url": reverse("epi:catalogo")},
        {"title": "Entregas de EPI", "desc": "Historico de entregas", "url": reverse("epi:listar")},
    ]
    return render(request, "gestao.html", {"cards": cards})


# ---------- Unidades ----------


@login_required
def unidades_list(request):
    unidades = Unidade.objects.all().order_by("nome")
    return render(request, "gestao/unidades_list.html", {"unidades": unidades})


@login_required
def unidade_create(request):
    if request.method == "POST":
        form = UnidadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gestao_unidades")
    else:
        form = UnidadeForm()
    return render(request, "gestao/form.html", {"form": form, "titulo": "Nova unidade"})


@login_required
def unidade_update(request, pk):
    unidade = get_object_or_404(Unidade, pk=pk)
    if request.method == "POST":
        form = UnidadeForm(request.POST, instance=unidade)
        if form.is_valid():
            form.save()
            return redirect("gestao_unidades")
    else:
        form = UnidadeForm(instance=unidade)
    return render(request, "gestao/form.html", {"form": form, "titulo": "Editar unidade"})


# ---------- Setores ----------


@login_required
def setores_list(request):
    setores = Setor.objects.select_related("unidade").all().order_by("nome")
    return render(request, "gestao/setores_list.html", {"setores": setores})


@login_required
def setor_create(request):
    if request.method == "POST":
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gestao_setores")
    else:
        form = SetorForm()
    return render(request, "gestao/form.html", {"form": form, "titulo": "Novo setor"})


@login_required
def setor_update(request, pk):
    setor = get_object_or_404(Setor, pk=pk)
    if request.method == "POST":
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            return redirect("gestao_setores")
    else:
        form = SetorForm(instance=setor)
    return render(request, "gestao/form.html", {"form": form, "titulo": "Editar setor"})


# ---------- Cargos ----------


@login_required
def cargos_list(request):
    cargos = Cargo.objects.all().order_by("titulo")
    return render(request, "gestao/cargos_list.html", {"cargos": cargos})


@login_required
def cargo_create(request):
    if request.method == "POST":
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gestao_cargos")
    else:
        form = CargoForm()
    return render(request, "gestao/form.html", {"form": form, "titulo": "Novo cargo"})


@login_required
def cargo_update(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == "POST":
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect("gestao_cargos")
    else:
        form = CargoForm(instance=cargo)
    return render(request, "gestao/form.html", {"form": form, "titulo": "Editar cargo"})


# ---------- Servidores ----------


@login_required
def servidores_list(request):
    servidores = (
        Servidor.objects.select_related("unidade", "setor", "cargo")
        .all()
        .order_by("nome")
    )
    return render(request, "gestao/servidores_list.html", {"servidores": servidores})


@login_required
def servidor_create(request):
    if request.method == "POST":
        form = ServidorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gestao_servidores")
    else:
        form = ServidorForm()
    return render(request, "gestao/form.html", {"form": form, "titulo": "Novo servidor"})


@login_required
def servidor_update(request, pk):
    servidor = get_object_or_404(Servidor, pk=pk)
    if request.method == "POST":
        form = ServidorForm(request.POST, instance=servidor)
        if form.is_valid():
            form.save()
            return redirect("gestao_servidores")
    else:
        form = ServidorForm(instance=servidor)
    return render(request, "gestao/form.html", {"form": form, "titulo": "Editar servidor"})


@require_POST
@login_required
def chat_api(request):
    """Endpoint de chat com IA baseada em NRs e contexto de navegacao."""
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalido."}, status=400)

    message = (payload.get("message") or "").strip()
    if not message:
        return JsonResponse({"error": "Mensagem vazia."}, status=400)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return JsonResponse({"error": "API nao configurada."}, status=503)

    client = OpenAI(api_key=api_key)
    system_prompt = (
        "Voce e um assistente de SST para prefeituras. Responda com base nas NRs vigentes "
        "(ex.: NR-01, NR-06 EPI, NR-07 PCMSO, NR-09 PGR, NR-10, NR-35) e cite a norma/artigo quando possivel. "
        "Se a pergunta for sobre navegacao no sistema, oriente o usuario aos modulos: Acidentes/CAT (S-2210), "
        "Exames (S-2220), EPI, Inspecoes, Treinamentos. Seja conciso."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            temperature=0.2,
            max_tokens=300,
        )
        answer = completion.choices[0].message.content
    except Exception:
        return JsonResponse({"error": "Falha ao consultar a IA."}, status=502)

    return JsonResponse({"answer": answer})
