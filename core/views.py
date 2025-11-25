from django.http import JsonResponse

def healthcheck(request):
    """Retorna status simples para validar deploy e integração."""
    return JsonResponse({"status": "ok"})
