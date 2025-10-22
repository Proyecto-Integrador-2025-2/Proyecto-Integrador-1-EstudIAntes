# chat/views.py
import json
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .services import get_completion
from .context_builders import fetch_user_context, build_prompt_for_routine
from .models import AISuggestion, RoutineSlot


# ------------------------------
# Página principal del módulo Chat
# ------------------------------
@login_required
def chat_home(request):
    """Pantalla principal del chat con formulario para hablar con la IA."""
    return render(request, "chat/ia_generate.html")


# ------------------------------
# Endpoint simple de consulta a la IA
# ------------------------------
def ai_query(request):
    """Endpoint POST: recibe 'prompt' y devuelve la respuesta de la IA en JSON."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    prompt = request.POST.get("prompt", "").strip()
    if not prompt:
        return JsonResponse({"error": "El prompt está vacío."}, status=400)

    try:
        system = "Eres un asistente breve y concreto. Responde en español."
        resp = get_completion(prompt, system=system)

        if not resp["ok"]:
            return JsonResponse({"error": resp["error"]}, status=500)

        return JsonResponse({"response": resp["text"]})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ------------------------------
# Generar sugerencias de rutina con IA
# ------------------------------
@login_required
def generate_routine_suggestions(request):
    """
    Llama a la IA con el contexto del usuario y guarda la sugerencia como AISuggestion.
    """
    try:
        ctx = fetch_user_context(request.user)
        prompt = build_prompt_for_routine(ctx)
        resp = get_completion(prompt)

        if not resp["ok"]:
            messages.error(request, resp["error"])
            return redirect("chat:home")

        # Intentar obtener el JSON generado
        data = resp["json"] or {}

        sug = AISuggestion.objects.create(
            user=request.user,
            kind="routine",
            payload=data or {"raw": resp["text"]},
        )

        messages.success(request, "Sugerencia generada correctamente.")
        return redirect("chat:view_suggestion", suggestion_id=sug.id)

    except Exception as e:
        messages.error(request, f"Error al generar sugerencia: {e}")
        return redirect("chat:home")


# ------------------------------
# Ver sugerencia generada por IA
# ------------------------------
@login_required
def view_suggestion(request, suggestion_id: int):
    sug = get_object_or_404(AISuggestion, id=suggestion_id, user=request.user)
    return render(request, "chat/suggestion_detail.html", {"suggestion": sug})


# ------------------------------
# Aplicar sugerencia (crear RoutineSlots)
# ------------------------------
@login_required
def apply_suggestion(request, suggestion_id: int):
    """
    Convierte la sugerencia en 'slots' de rutina editables (RoutineSlot).
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    sug = get_object_or_404(AISuggestion, id=suggestion_id, user=request.user)
    suggestions = sug.payload.get("suggestions", []) or sug.payload.get("slots", [])

    count = 0
    for s in suggestions:
        day = s.get("day")
        start = s.get("start")
        end = s.get("end")
        activity = s.get("activity", "Estudio")
        notes = s.get("notes", "")

        try:
            start_t = datetime.strptime(start, "%H:%M").time()
            end_t = datetime.strptime(end, "%H:%M").time()
        except Exception:
            continue

        RoutineSlot.objects.create(
            user=request.user,
            day=day,
            start=start_t,
            end=end_t,
            activity=activity,
            notes=notes,
            source="ai",
        )
        count += 1

    sug.applied = True
    sug.save(update_fields=["applied"])

    messages.success(request, f"Se aplicaron {count} bloques a tu rutina.")
    return redirect('routine')


# ------------------------------
# Ver los RoutineSlots aplicados
# ------------------------------
@login_required
def list_routine_slots(request):
    slots = RoutineSlot.objects.filter(user=request.user).order_by("day", "start")
    return render(request, "chat/routine_slots.html", {"slots": slots})
