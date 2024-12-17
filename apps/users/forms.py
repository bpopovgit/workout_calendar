import random
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'password2': 'Repeat Password',  # Rename the field label
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        # Custom password requirements
        if len(password1) < 8:
            errors.append("Your password must contain at least 8 characters.")
        if password1.isnumeric():
            errors.append("Your password cannot be entirely numeric.")
        if password1.lower() in ['password', '12345678']:
            errors.append("Your password cannot be a commonly used password.")

        if errors:
            raise forms.ValidationError(random.choice(errors))  # Display a random error
        return password1
