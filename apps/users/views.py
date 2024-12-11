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


def profile_view(request):
    user = request.user
    welcome_message = f"Welcome, {user.first_name} {user.last_name}"

    # Adjusted logic for recent/completed workouts
    recent_workouts = WorkoutLog.objects.filter(
        user=user,
        date_completed__gte=date.today() - timedelta(days=7)  # Example: last 7 days
    ).order_by('-date_completed')

    # Calculate completed workouts and hours spent
    completed_workouts = WorkoutLog.objects.filter(user=user).count()
    hours_spent = WorkoutLog.objects.filter(user=user).aggregate(total_hours=Sum('workout__duration'))[
                      'total_hours'] or 0

    # Fetch active goals
    active_goals = Goal.objects.filter(user=user, is_active=True)

    return render(request, 'users/profile.html', {
        'welcome_message': welcome_message,
        'recent_workouts': recent_workouts,  # Pass recent/completed workouts
        'completed_workouts': completed_workouts,
        'hours_spent': hours_spent,
        'active_goals': active_goals,
    })


# Example logic for fetching upcoming workouts
def get_upcoming_workouts(user, limit=5):
    today = datetime.now().date()
    return WorkoutSchedule.objects.filter(user=user, date__gte=today).order_by('date')[:limit]


def user_profile_view(request):
    user = request.user

    # Upcoming workouts
    upcoming_workouts = get_upcoming_workouts(user)

    # Other sections (e.g., recent workouts, progress)
    # Assuming similar logic is already implemented

    context = {
        'user': user,
        'upcoming_workouts': upcoming_workouts,
        # Add other sections (recent_workouts, progress, etc.)
    }
    return render(request, 'users/profile.html', context)