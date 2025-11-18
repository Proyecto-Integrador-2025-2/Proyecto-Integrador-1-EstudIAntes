from django import forms
from .models import ClassSchedule, AvailableBlock


class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['day', 'start_time', 'end_time', 'subject']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-sm'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-sm'}),
            'subject': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get("day")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("La hora de inicio debe ser antes que la hora de fin.")

        if day and start_time and end_time:
            # Buscar traslape con otros horarios ocupados DEL MISMO USUARIO
            overlaps = ClassSchedule.objects.filter(
                day=day,
                start_time__lt=end_time,   # empieza antes de que termine este
                end_time__gt=start_time    # termina después de que empiece este
            )
            
            # Filtrar por usuario si está disponible
            if self.user:
                overlaps = overlaps.filter(user=self.user)

            # Excluirse a sí mismo si está editando
            if self.instance and self.instance.pk:
                overlaps = overlaps.exclude(pk=self.instance.pk)

            if overlaps.exists():
                conflict = overlaps.first()
                raise forms.ValidationError(
                    f"Conflicto con {conflict.subject or 'otro horario'}: "
                    f"{conflict.start_time.strftime('%I:%M %p')} - {conflict.end_time.strftime('%I:%M %p')}."
                )

        return cleaned_data


class AvailableBlockForm(forms.ModelForm):
    class Meta:
        model = AvailableBlock
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-sm'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get("day")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("La hora de inicio debe ser antes que la hora de fin.")

        if day and start_time and end_time:
            # Buscar traslape con horarios ocupados DEL MISMO USUARIO
            overlaps = ClassSchedule.objects.filter(
                day=day,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            # Filtrar por usuario si está disponible
            if self.user:
                overlaps = overlaps.filter(user=self.user)

            if self.instance and self.instance.pk:
                overlaps = overlaps.exclude(pk=self.instance.pk)

            if overlaps.exists():
                conflict = overlaps.first()
                raise forms.ValidationError(
                    f"Ya tienes un horario ocupado que se solapa: {conflict.subject or 'otro horario'} "
                    f"({conflict.start_time.strftime('%I:%M %p')} - {conflict.end_time.strftime('%I:%M %p')})."
                )

        return cleaned_data
