from datetime import date, timedelta, datetime

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Sum, Count
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import now
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponse
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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True  # Activate the account immediately
        user.save()

        # Commented-out email verification logic
        """
        # Deactivate account until email is confirmed
        user.is_active = False  
        user.save()

        # Generate email verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = self.request.build_absolute_uri(
            reverse('users:email_verify', kwargs={'uidb64': uid, 'token': token})
        )

        # Send verification email
        subject = "Activate Your Account"
        message = render_to_string('users/verify_email.html', {
            'user': user,
            'confirm_url': confirm_url,
        })
        send_mail(subject, message, 'noreply@tempotrack.com', [user.email])

        messages.success(self.request, 'Please check your email to confirm your registration.')
        """

        messages.success(self.request, 'Your account has been created successfully! You can now log in.')
        return redirect('login')


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


@login_required
def user_profile_view(request):
    user = request.user

    # Total Workouts Completed
    total_completed_workouts = WorkoutSchedule.objects.filter(user=user, completed=True).count()

    # Total Hours Spent Exercising (Sum of durations)
    total_duration = WorkoutSchedule.objects.filter(user=user, completed=True).aggregate(
        total_duration=Sum('workout__duration')
    )['total_duration']

    # Weekly Schedule (Upcoming Workouts for this week)
    today = timezone.now().date()
    weekly_schedule = WorkoutSchedule.objects.filter(
        user=user,
        date__gte=today,
        date__lte=today + timezone.timedelta(days=7)
    ).order_by('date')

    context = {
        'total_completed_workouts': total_completed_workouts,
        'total_hours_spent': total_duration.total_seconds() / 3600 if total_duration else 0,
        'weekly_schedule': weekly_schedule,
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


def email_verify(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully! You can now log in.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid or has expired.')
