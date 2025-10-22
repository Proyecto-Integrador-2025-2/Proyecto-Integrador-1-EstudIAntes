# busyschedule/views.py
from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

from .forms import ClassScheduleForm, AvailableBlockForm
from .models import ClassSchedule, AvailableBlock, DAYS
from chat.models import RoutineSlot


# ===============================================================
# 🔹 FUNCIONES AUXILIARES
# ===============================================================

def merge_available_blocks(day):
    """Une bloques disponibles que se solapan en un mismo día."""
    blocks = AvailableBlock.objects.filter(day=day).order_by('start_time')
    merged = []
    for block in blocks:
        if not merged or merged[-1].end_time < block.start_time:
            merged.append(block)
        else:
            merged[-1].end_time = max(merged[-1].end_time, block.end_time)
            merged[-1].save()
            block.delete()


# ===============================================================
# 🔹 INICIO / CALENDARIO VISUAL
# ===============================================================

def main_home(request):
    """Vista principal (inicio): muestra un calendario visual con bloques y horarios."""
    schedules = ClassSchedule.objects.all().order_by('day', 'start_time')
    blocks = AvailableBlock.objects.all().order_by('day', 'start_time')

    days = [d[0] for d in DAYS]  # ["Lunes", "Martes", ...]
    hours = list(range(8, 23))

    is_empty = not (schedules.exists() or blocks.exists())

    # Si está vacío, no construimos la tabla
    rows_html = []
    if not is_empty:
        for s in schedules:
            s.rowspan = max(1, s.end_time.hour - s.start_time.hour)
        for b in blocks:
            b.rowspan = max(1, b.end_time.hour - b.start_time.hour)

        # Construimos las filas del calendario ya renderizadas (HTML)
        occupied = {day: 0 for day in days}
        for hour in hours:
            cells = []
            for day in days:
                if occupied.get(day, 0) > 0:
                    occupied[day] -= 1
                    continue

                start_schedule = next((x for x in schedules if x.day == day and x.start_time.hour == hour), None)
                if start_schedule:
                    rowspan = start_schedule.rowspan
                    occupied[day] = max(0, rowspan - 1)
                    td = f'<td class="bg-danger text-white align-middle text-center" rowspan="{rowspan}">{start_schedule.subject or "Clase"}</td>'
                    cells.append(td)
                    continue

                start_block = next((x for x in blocks if x.day == day and x.start_time.hour == hour), None)
                if start_block:
                    rowspan = start_block.rowspan
                    occupied[day] = max(0, rowspan - 1)
                    td = f'<td class="bg-success text-white align-middle text-center" rowspan="{rowspan}">Disponible</td>'
                    cells.append(td)
                    continue

                cells.append('<td class="bg-white"></td>')

            row_html = f'<tr><th scope="row">{hour}:00</th>' + ''.join(cells) + '</tr>'
            rows_html.append(row_html)

    return render(request, "calendar_view.html", {
        "rows_html": rows_html,
        "hours": hours,
        "days": days,
        "schedules": schedules,
        "blocks": blocks,
        "is_empty": is_empty,
    })



# ===============================================================
# 🔹 GESTIÓN DE HORARIOS (CRUD + FORMULARIOS)
# ===============================================================

@login_required
@login_required
def schedule_home(request):
    # Query de datos para la página
    schedules = sorted(
        ClassSchedule.objects.all(),
        key=lambda s: (s.day_index(), s.start_time)
    )
    blocks = sorted(
        AvailableBlock.objects.all(),
        key=lambda b: (b.day_index(), b.start_time)
    )

    # Agrupar bloques por día para el template
    blocks_by_day = defaultdict(list)
    for b in blocks:
        blocks_by_day[b.day].append(b)

    # ⚠️ Inicializa SIEMPRE ambos formularios para evitar UnboundLocalError
    form_schedule = ClassScheduleForm()
    form_block = AvailableBlockForm()

    if request.method == "POST":
        # ---- Crear HORARIO OCUPADO ----
        if "save_schedule" in request.POST:
            form_schedule = ClassScheduleForm(request.POST)
            if form_schedule.is_valid():
                obj = form_schedule.save(commit=False)
                # Si el modelo tiene campo user, asígnalo
                if hasattr(obj, "user") and request.user.is_authenticated:
                    obj.user = request.user
                obj.save()

                # Eliminar bloques disponibles que se solapen
                overlapping = AvailableBlock.objects.filter(
                    day=obj.day,
                    start_time__lt=obj.end_time,
                    end_time__gt=obj.start_time
                )
                removed = overlapping.count()
                if removed:
                    overlapping.delete()
                    messages.info(request, f"Se eliminaron {removed} bloque(s) disponibles por conflicto con '{obj.subject}'.")
                messages.success(request, "Horario agregado correctamente.")
                return redirect("busyschedule:schedule_home")
            # Si es inválido, cae a render con errores usando form_schedule + form_block vacío

        # ---- Crear BLOQUE DISPONIBLE ----
        elif "save_block" in request.POST:
            form_block = AvailableBlockForm(request.POST)
            if form_block.is_valid():
                blk = form_block.save(commit=False)
                if hasattr(blk, "user") and request.user.is_authenticated:
                    blk.user = request.user
                blk.save()

                # Unificar bloques solapados (si tienes la función)
                try:
                    from .views import merge_available_blocks
                    merge_available_blocks(blk.day)
                except Exception:
                    pass

                messages.success(request, "Bloque disponible agregado correctamente.")
                return redirect("busyschedule:schedule_home")
            # Si es inválido, cae a render con errores usando form_block + form_schedule vacío

        # Si llega otro botón/acción no reconocida, simplemente re-renderiza con lo ya capturado

    # GET o POST inválido → render con formularios (válidos o con errores)
    return render(request, "home.html", {
        "schedules": schedules,
        "blocks_by_day": dict(blocks_by_day),
        "form_schedule": form_schedule,
        "form_block": form_block,
    })
# ===============================================================
# 🔹 EDITAR / ELIMINAR HORARIOS Y BLOQUES
# ===============================================================

@login_required
def edit_schedule_modal(request, pk):
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            updated_schedule = form.save()

            overlapping_blocks = AvailableBlock.objects.filter(
                day=updated_schedule.day,
                start_time__lt=updated_schedule.end_time,
                end_time__gt=updated_schedule.start_time
            )
            deleted_count = overlapping_blocks.count()
            overlapping_blocks.delete()

            if deleted_count > 0:
                return JsonResponse({
                    "success": True,
                    "message": f"{deleted_count} bloque(s) eliminado(s) por conflicto con '{updated_schedule.subject}'."
                })
            return JsonResponse({"success": True})
        else:
            html_form = render_to_string("edit_form.html", {"form": form, "schedule": schedule}, request=request)
            return JsonResponse({"success": False, "html_form": html_form})
    else:
        form = ClassScheduleForm(instance=schedule)
        html_form = render_to_string("edit_form.html", {"form": form, "schedule": schedule}, request=request)
        return JsonResponse({"html_form": html_form})


@login_required
def delete_schedule(request, pk):
    sched = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == "POST":
        sched.delete()
        messages.success(request, "Horario eliminado correctamente.")
        return redirect('busyschedule:schedule_home')
    # Si alguien entra por GET, muestra una confirmación simple o redirige:
    return redirect('busyschedule:schedule_home')

@login_required
def delete_block(request, pk):
    blk = get_object_or_404(AvailableBlock, pk=pk)
    if request.method == "POST":
        blk.delete()
        messages.success(request, "Bloque disponible eliminado correctamente.")
        return redirect('busyschedule:schedule_home')
    return redirect('busyschedule:schedule_home')


# ===============================================================
# 🔹 VISTA DE RUTINA (IA)
# ===============================================================

def routine_view(request):
    """
    Muestra los horarios sugeridos por la IA o los aplicados por el usuario.
    """
    schedules = ClassSchedule.objects.all()
    blocks = AvailableBlock.objects.all()
    routine_slots = RoutineSlot.objects.filter(user=request.user) if request.user.is_authenticated else RoutineSlot.objects.none()

    # Intervalos de 1 hora (8 a 22)
    hours = list(range(8, 23))
    days = [d[0] for d in DAYS]

    for s in schedules:
        s.rowspan = max(1, s.end_time.hour - s.start_time.hour)
    for b in blocks:
        b.rowspan = max(1, b.end_time.hour - b.start_time.hour)

    is_empty = not (routine_slots.exists())

    return render(request, "routine.html", {
        "schedules": schedules,
        "blocks": blocks,
        "hours": hours,
        "days": days,
        "routine_slots": routine_slots,
        "is_empty": is_empty,
    })


