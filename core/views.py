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
            "slug": "S-2210",
            "description": "Registros CAT e S-2210",
            "url": reverse("acidentes:index"),
        },
        {
            "name": "Gestão",
            "slug": "Cadastros",
            "description": "Cadastros de servidores, EPIs, unidades e setores",
            "url": reverse("gestao"),
        },
        {"name": "EPI", "slug": "NR-06", "description": "Controle de EPIs e entregas", "url": reverse("epi:index")},
        {"name": "Exames", "slug": "S-2220", "description": "Gestão de exames S-2220", "url": reverse("exames:index")},
        {"name": "Relatórios", "slug": "Dashboards", "description": "PDFs e indicadores", "url": reverse("relatorios")},
        {"name": "Inspeções", "slug": "Checklists", "description": "Não conformidades e planos", "url": None},
        {"name": "Treinamentos", "slug": "Cursos", "description": "Turmas, certificados e validade", "url": None},
    ]
    return render(request, "home.html", {"modules": modules})


@login_required
def relatorios(request):
    """Landing de relatórios com atalhos para indicadores e exports."""
    reports = [
        {
            "title": "Relatórios de Saúde do Trabalho",
            "desc": "Exames (S-2220), ASO, vencimentos, afastamentos e indicadores de PCMSO.",
            "cta": "Abrir Saúde do Trabalho",
            "url": reverse("relatorios_saude"),
        },
        {
            "title": "Relatórios de Segurança do Trabalho",
            "desc": "Acidentes (S-2210), EPI, treinamentos por NR, inspeções e planos de ação.",
            "cta": "Abrir Segurança do Trabalho",
            "url": reverse("relatorios_seguranca"),
        },
    ]
    return render(request, "relatorios.html", {"reports": reports})


@login_required
def relatorios_saude(request):
    """Relatórios focados em saúde (S-2220/PCMSO)."""
    reports = [
        {"title": "Exames (S-2220)", "desc": "Período, status, vencimentos de ASO."},
        {"title": "Afastamentos", "desc": "Motivo, datas e CID."},
        {"title": "Indicadores PCMSO", "desc": "Taxas, pendências e vencimentos."},
    ]
    return render(request, "relatorios_saude.html", {"reports": reports})


@login_required
def relatorios_seguranca(request):
    """Relatórios focados em segurança (S-2210/GRO/PGR)."""
    reports = [
        {"title": "Acidentes / CAT (S-2210)", "desc": "Período, unidade, setor, CID."},
        {"title": "EPI", "desc": "Entregas, CA e validade."},
        {"title": "Treinamentos", "desc": "Validade por NR e unidade."},
        {"title": "Inspeções e Planos", "desc": "Não conformidades e status."},
    ]
    return render(request, "relatorios_seguranca.html", {"reports": reports})


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

    api_key = (os.getenv("OPENAI_API_KEY"))
    if not api_key:
        return JsonResponse({"error": "API nao configurada."}, status=503)

    client = OpenAI(api_key=api_key)
    system_prompt = (
        "Voce e um assistente SENIOR de SST para prefeituras, orgãos governamentais, hospitais e empresas, "
        "tambem atuando como guia do sistema web SST_GOV. "
        "Estilo de resposta: seja objetivo e didatico; quando a duvida for sobre uso do sistema, responda em passos numerados sem asteriscos "
        "(Passo 1, Passo 2...) dizendo exatamente onde clicar, que rota abrir e quais campos preencher. "
        "Para duvidas normativas, responda diretamente citando a NR (NR-01, NR-06 EPI, NR-07 PCMSO, NR-09 PGR, NR-10, NR-18, NR-35 etc.) "
        "e artigo/item sempre que possivel. "
        "Contexto do sistema: Home tem cards para Acidentes/CAT (S-2210), EPI (entregas e catalogo), Gestao "
        "(Servidores, Unidades, Setores, Cargos, EPIs, Entregas), Exames (S-2220), Inspecoes, Treinamentos, Relatorios. "
        "Rotas uteis: /gestao/ (atalhos de cadastros), /epi/catalogo/ (cadastro de EPIs), /epi/listar/ (entregas), "
        "/acidentes/ (dashboard acidentes) e /acidentes/listar/, /relatorios/ (Saude e Seguranca). "
        "Regras de atendimento: "
        "1) Se for navegacao, priorize orientar dentro do sistema com passos detalhados. "
        "2) Se for norma, cite a NR pertinente e mantenha a resposta curta e acionavel. "
        "3) Se for eSocial, contextualize S-2210 (CAT), S-2220 (exames) e S-2240 (riscos) com cuidados de preenchimento. "
        "4) Se houver duvida ambigua, peça 1 clarificacao rapida e sugira o dado que falta (ex.: período, unidade, setor). "
        "5) Nao invente dados da organizacao; use apenas o que for informado pelo usuario."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            temperature=0.2,
            max_tokens=15000,
        )
        answer = completion.choices[0].message.content
    except Exception:
        return JsonResponse({"error": "Falha ao consultar a IA."}, status=502)

    return JsonResponse({"answer": answer})

