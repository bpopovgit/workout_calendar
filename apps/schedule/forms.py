from django import forms
from .models import WorkoutSchedule
from django import forms
from .models import Measurement


class WorkoutScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkoutSchedule
        fields = ['workout', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',  # Use HTML5 date input for better UX
                'placeholder': 'YYYY-MM-DD',  # Provide a placeholder for the user
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',  # Use HTML5 time input for better UX
            }),
        }
        help_texts = {
            'date': 'Enter the date in the format YYYY-MM-DD.',
        }


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['weight', 'chest', 'arm', 'waist', 'hips', 'thighs', 'calf', 'bmi']
