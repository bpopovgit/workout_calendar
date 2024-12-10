from django.db import models
from django.contrib.auth.models import User
from apps.workouts.models import Workout


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date_completed = models.DateTimeField()  # Removed `editable=False`
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.workout.name} - {self.date_completed}"


class Progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="progress")
    total_workouts_completed = models.PositiveIntegerField(default=0)
    total_duration = models.DurationField(default="0:00:00")

    def __str__(self):
        return f"{self.user.username}'s Progress"


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(max_length=255)
    target = models.FloatField()  # e.g., number of workouts, hours, distance
    progress = models.FloatField(default=0)  # Current progress toward the target
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
