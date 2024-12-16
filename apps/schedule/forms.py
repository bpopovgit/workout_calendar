from django import forms
from .models import WorkoutSchedule
from django import forms
from .models import Measurement
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

from ..workouts.models import Workout


class WorkoutScheduleForm(forms.ModelForm):
    workout = forms.ModelChoiceField(
        queryset=Workout.objects.none(),  # Default queryset is empty
        label="Workout",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = WorkoutSchedule
        fields = ['workout', 'date', 'time', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add a description for this workout (optional).'
            }),
        }
        help_texts = {
            'description': 'Provide additional details about this workout schedule.',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the logged-in user
        super().__init__(*args, **kwargs)
        if user:
            # Filter workouts to only those created by the logged-in user
            self.fields['workout'].queryset = Workout.objects.filter(user=user)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))


class EditWorkoutScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkoutSchedule
        fields = ['workout', 'time', 'description']  # Exclude 'date'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Pass the user to filter workouts
        super().__init__(*args, **kwargs)

        # Filter the workout field to only show workouts belonging to the current user
        self.fields['workout'].queryset = Workout.objects.filter(user=user)

        # Apply widget attributes
        self.fields['workout'].widget.attrs.update({'class': 'form-select'})
        self.fields['time'].widget.attrs.update({'class': 'form-control', 'type': 'time'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 3})

        # Optional: Include 'date' as a readonly field
        self.fields['date'] = forms.CharField(
            initial=self.instance.date,
            widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
        )


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['weight', 'chest', 'arm', 'waist', 'hips', 'thighs', 'calf', 'bmi']
