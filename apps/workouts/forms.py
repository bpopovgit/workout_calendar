from django import forms
from django_select2.forms import Select2MultipleWidget

from .models import Workout


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'exercises', 'duration', 'intensity']
        widgets = {
            'exercises': Select2MultipleWidget,  # Use Select2 for the exercises field
        }