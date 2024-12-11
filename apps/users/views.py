from datetime import date, timedelta, datetime
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
from ..progress.models import WorkoutLog, Goal
from ..schedule.models import WorkoutSchedule
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


# Example logic for fetching upcoming workouts
def get_upcoming_workouts(user, limit=5):
    now = datetime.now()  # Ensure it gets the current date and time
    # Filter workouts that are in the future
    workouts = WorkoutSchedule.objects.filter(
        user=user,
        date__gte=now.date()
    ).order_by('date', 'time')

    upcoming = []
    for workout in workouts:
        workout_datetime = datetime.combine(workout.date, workout.time)
        if workout_datetime >= now:  # Ensure the workout is truly in the future
            workout.overdue = False
            upcoming.append(workout)
        else:
            workout.overdue = True  # This shouldn't trigger for future workouts

    return upcoming[:limit]


def user_profile_view(request):
    user = request.user
    upcoming_workouts = get_upcoming_workouts(user)

    context = {
        'upcoming_workouts': upcoming_workouts,
        # Include other context variables (recent_workouts, progress, etc.)
    }
    return render(request, 'users/profile.html', context)
