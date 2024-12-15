from datetime import date, timedelta, datetime
from django.db.models import Sum
from django.utils import timezone
from django.utils.timezone import now
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
from django.http import Http404, JsonResponse
from ..goals.models import WorkoutLog, Goal
from ..schedule.models import WorkoutSchedule
from ..workouts.models import Workout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages


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

    # Existing logic for upcoming workouts
    upcoming_workouts = get_upcoming_workouts(user)

    # Add logic for recent workouts
    recent_workouts = get_recent_workouts(user)

    context = {
        'upcoming_workouts': upcoming_workouts,
        'recent_workouts': recent_workouts,
        # Add other context variables like goals, goals, etc.
    }
    return render(request, 'users/profile.html', context)


def get_recent_workouts(user, limit=5):
    """Fetches the most recent completed workouts."""
    return (
        WorkoutLog.objects.filter(user=user)
        .order_by('-date_completed')[:limit]  # Sort by the latest completion date
    )


def get_workout_data(request):
    user = request.user
    today = datetime.now().date()

    # Fetch recent workouts
    recent_workouts = WorkoutLog.objects.filter(user=user).order_by('-date_completed')[:5]

    # Fetch upcoming workouts
    upcoming_workouts = WorkoutSchedule.objects.filter(user=user, date__gte=today).order_by('date', 'time')[:5]

    # Serialize data for Chart.js
    recent_data = [
        {
            "label": workout.workout.name,
            "date": workout.date_completed.strftime('%Y-%m-%d'),
            "intensity": workout.intensity,
        }
        for workout in recent_workouts
    ]

    upcoming_data = [
        {
            "label": workout.workout.name,
            "date": workout.date.strftime('%Y-%m-%d'),
            "intensity": workout.intensity,
        }
        for workout in upcoming_workouts
    ]

    return JsonResponse({
        "recent_workouts": recent_data,
        "upcoming_workouts": upcoming_data,
    })

@login_required
def edit_profile(request):
    user = request.user
    profile = UserProfile.objects.get_or_create(user=user)[0]  # Ensure profile exists

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_picture = request.FILES.get('profile_picture')
        goal = request.POST.get('goal')

        # Update user email
        if email:
            user.email = email

        # Update user password
        if password:
            user.set_password(password)

        # Update profile fields
        if profile_picture:
            profile.profile_picture = profile_picture
        if goal:
            profile.goal = goal

        user.save()
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')

    return render(request, 'users/edit_profile.html', {'profile': profile})