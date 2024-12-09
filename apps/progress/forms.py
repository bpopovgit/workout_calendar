from django import forms
from .models import WorkoutLog


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
