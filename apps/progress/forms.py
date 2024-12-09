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
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Run 5 miles'}),
            'target': forms.NumberInput(attrs={'placeholder': 'e.g., 5'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }