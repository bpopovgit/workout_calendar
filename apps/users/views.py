from datetime import date

from django.db.models import Sum
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from ..progress.models import WorkoutLog
from ..workouts.models import Workout


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        try:
            return self.request.user.userprofile
        except UserProfile.DoesNotExist:
            raise Http404("UserProfile does not exist. Please contact support.")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    # Allows the logged-in user to update their profile.
    model = UserProfile
    fields = ['goal', 'profile_picture']
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        # Return the UserProfile for the currently logged-in user
        return UserProfile.objects.get(user=self.request.user)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')


def profile_view(request):
    user = request.user
    welcome_message = f"Welcome, {user.first_name} {user.last_name}"
    upcoming_workouts = Workout.objects.filter(user=user, date__gte=date.today()).order_by('date')
    completed_workouts = WorkoutLog.objects.filter(user=user).count()
    hours_spent = WorkoutLog.objects.filter(user=user).aggregate(total_hours=Sum('duration'))['total_hours'] or 0

    return render(request, 'users/profile.html', {
        'welcome_message': welcome_message,
        'upcoming_workouts': upcoming_workouts,
        'completed_workouts': completed_workouts,
        'hours_spent': hours_spent,
    })