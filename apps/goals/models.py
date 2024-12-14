from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from apps.workouts.models import Workout


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_logs")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date_completed = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    intensity = models.CharField(
        max_length=50,
        choices=[
            ('Low', 'Low'),
            ('Moderate', 'Moderate'),
            ('High', 'High'),
        ],
        default='Moderate'
    )

    def __str__(self):
        return f"{self.workout.name} ({self.date_completed})"


class Progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="goals")
    total_workouts_completed = models.PositiveIntegerField(default=0)
    total_duration = models.DurationField(default="0:00:00")

    def __str__(self):
        return f"{self.user.username}'s Progress"


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_goals')  # Updated related_name
    name = models.CharField(max_length=255)
    target = models.FloatField()
    progress = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def percentage_complete(self):
        if self.target == 0:
            return 0
        return (self.progress / self.target) * 100


class UpdateProgressView(LoginRequiredMixin, UpdateView):
    model = Goal
    fields = ['progress']
    template_name = 'goals/update_progress.html'
    context_object_name = 'goal'
    success_url = reverse_lazy('goals:goal_list')

    def get_queryset(self):
        # Ensure only the user's goals can be updated
        return Goal.objects.filter(user=self.request.user)
