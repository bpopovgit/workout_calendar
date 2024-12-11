from django import forms
from .models import WorkoutSchedule
from django import forms
from .models import Measurement


class WorkoutScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkoutSchedule
        fields = ['workout', 'date', 'time']


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['weight', 'chest', 'arm', 'waist', 'hips', 'thighs', 'calf', 'bmi']
