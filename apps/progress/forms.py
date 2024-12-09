from django import forms
from .models import WorkoutLog, Goal


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'target', 'due_date']
