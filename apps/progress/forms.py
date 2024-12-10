from django import forms
from .models import WorkoutLog, Goal
from ..workouts.models import Workout


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout', 'date_completed', 'notes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the 'user' parameter
        super().__init__(*args, **kwargs)
        if user:
            # Filter the workout field to show only the workouts created by the logged-in user
            self.fields['workout'].queryset = Workout.objects.filter(user=user)


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'target', 'due_date']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Run 5 miles'}),
            'target': forms.NumberInput(attrs={'placeholder': 'e.g., 5'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }