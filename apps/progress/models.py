from django.db import models
from django.contrib.auth.models import User
from apps.workouts.models import Workout


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date_completed = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout.name} on {self.date_completed}"


class Progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workouts_completed = models.PositiveIntegerField(default=0)
    total_duration = models.DurationField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Progress"
