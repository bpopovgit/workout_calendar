from django import forms
from .models import WorkoutSchedule
from django import forms
from .models import Measurement


class WorkoutScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkoutSchedule
        fields = ['workout', 'date', 'time', 'description']  # Include the description field
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3,
                                                 'placeholder': 'Add a description for this workout (optional).'}),
        }
        help_texts = {
            'description': 'Provide additional details about this workout schedule.',
        }


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['weight', 'chest', 'arm', 'waist', 'hips', 'thighs', 'calf', 'bmi']
