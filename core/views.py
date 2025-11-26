import json
import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from openai import OpenAI


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


@require_POST
@login_required
def chat_api(request):
    """Endpoint de chat com IA baseada em NRs e contexto de navegação."""
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400)

    message = (payload.get("message") or "").strip()
    if not message:
        return JsonResponse({"error": "Mensagem vazia."}, status=400)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return JsonResponse({"error": "API não configurada."}, status=503)

    client = OpenAI(api_key=api_key)
    system_prompt = (
        "Você é um assistente de SST para prefeituras. Responda com base nas NRs vigentes "
        "(ex.: NR-01, NR-06 EPI, NR-07 PCMSO, NR-09 PGR, NR-10, NR-35) e cite a norma/artigo quando possível. "
        "Se a pergunta for sobre navegação no sistema, oriente o usuário aos módulos: Acidentes/CAT (S-2210), "
        "Exames (S-2220), EPI, Inspeções, Treinamentos. Seja conciso."
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
