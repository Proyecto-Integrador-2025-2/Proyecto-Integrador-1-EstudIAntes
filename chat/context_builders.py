# chat/context_builders.py
from typing import List, Dict
from django.contrib.auth.models import User
from busyschedule.models import ClassSchedule, AvailableBlock

DAYS_ES = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

def fetch_user_context(user: User) -> Dict:
    # Ajusta si los modelos tienen relación con usuario (user=ForeignKey). 
    # Si aún no, filtra global o adapta cuando agreguen multiusuario.
    schedules = ClassSchedule.objects.all().order_by("day", "start_time")
    blocks = AvailableBlock.objects.all().order_by("day", "start_time")

    def fmt_slot(s):
        return {
            "day": s.day,  # Asumes 'Lunes', 'Martes', etc.
            "start": s.start_time.strftime("%H:%M"),
            "end": s.end_time.strftime("%H:%M"),
            "subject": getattr(s, "subject", None)
        }

    return {
        "user": {"username": user.username if user.is_authenticated else "anon"},
        "occupied": [fmt_slot(s) for s in schedules],
        "available": [fmt_slot(b) for b in blocks],
        # Si luego agregan tareas (Sprint 2), las añadimos aquí.
        "tasks": []  # placeholder
    }

def build_prompt_for_routine(context: Dict) -> str:
    """
    Construye un prompt legible para el LLM:
    - Ocupados
    - Libres
    - Objetivo: proponer rutina breve y priorizada
    - Formato de respuesta estructurado
    """
    occ_lines = []
    for s in context["occupied"]:
        occ_lines.append(f"- {s['day']} {s['start']}-{s['end']} {('('+s['subject']+')') if s['subject'] else ''}".strip())

    free_lines = []
    for b in context["available"]:
        free_lines.append(f"- {b['day']} {b['start']}-{b['end']}")

    return f"""
Eres un asistente que organiza estudio. Con base en:
HORARIOS OCUPADOS:
{chr(10).join(occ_lines) if occ_lines else '- (sin clases registradas)'}
BLOQUES LIBRES:
{chr(10).join(free_lines) if free_lines else '- (sin bloques disponibles)'}
TAREAS (si existieran): {len(context.get('tasks', []))}

Objetivo:
1) Propón una rutina de estudio para los próximos 7 días, usando solo los bloques libres.
2) Prioriza por urgencia y balance (no sobrecargar, incluye pausas).
3) Devuelve la salida en JSON con este formato EXACTO:

{{
  "suggestions": [
    {{
      "day": "Lunes|Martes|...",
      "start": "HH:MM",
      "end": "HH:MM",
      "activity": "Estudiar X / Repasar Y / Pausa activa ...",
      "notes": "Opcional: breve razón o prioridad"
    }}
  ],
  "summary": "1-2 frases resumiendo la estrategia"
}}

Solo JSON válido, sin comentarios adicionales.
""".strip()
