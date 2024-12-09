from django.db import models
from django.contrib.auth.models import User
from apps.workouts.models import Workout


class WorkoutSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="schedules")
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.workout.name} on {self.date} at {self.time}"
