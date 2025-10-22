from django.db import models
from django.contrib.auth.models import User

class AISuggestion(models.Model):
    KIND_CHOICES = (
        ("routine", "Routine"),
        ("priority", "Priority"),
        ("advice", "Advice"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    kind = models.CharField(max_length=32, choices=KIND_CHOICES, default="routine")
    payload = models.JSONField()  # JSON devuelto por la IA (suggestions[], summary)
    created_at = models.DateTimeField(auto_now_add=True)
    applied = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.kind}] {self.user or 'anon'} @ {self.created_at:%Y-%m-%d %H:%M}"

class RoutineSlot(models.Model):
    """
    Si quieres 'materializar' la rutina como entidad propia editable
    (distinta a AvailableBlock). Puedes usarla como calendario de estudio.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    day = models.CharField(max_length=16)       # 'Lunes', 'Martes', ...
    start = models.TimeField()
    end = models.TimeField()
    activity = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    source = models.CharField(max_length=32, default="ai")  # 'ai' o 'manual'
    created_at = models.DateTimeField(auto_now_add=True)
