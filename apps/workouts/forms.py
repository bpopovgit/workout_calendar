from datetime import timedelta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Column, Row
from django import forms
from django_select2.forms import Select2MultipleWidget
from .models import Workout, Exercise


class WorkoutForm(forms.ModelForm):
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        label="Select Exercises",
    )
    # Override duration field to accept input in minutes
    duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration in minutes'}),
        label="Duration (in minutes)",
    )

    class Meta:
        model = Workout
        fields = ['name', 'exercises', 'duration', 'intensity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('duration', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('intensity', css_class='form-group col-md-6 mb-0'),
                Column('exercises', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.add_input(Submit('submit', 'Save Workout', css_class='btn-primary'))

    def clean_duration(self):
        # Convert minutes to seconds before saving to the database
        duration_in_minutes = self.cleaned_data['duration']
        return timedelta(minutes=duration_in_minutes) # Returns a timedelta object,
        # which ensures that the input is correctly formatted for Django's DurationField.
