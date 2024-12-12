from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django_select2.forms import Select2MultipleWidget

from .models import Workout


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'exercises', 'duration', 'intensity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Workout', css_class='btn-primary'))

