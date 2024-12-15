from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from apps.workouts.models import Workout


class WorkoutSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.workout.name} on {self.date} at {self.time}"

    @property
    def intensity(self):
        """
        Fetch the intensity from the related Workout model.
        """
        return self.workout.intensity

    @property
    def formatted_date_time(self):
        """
        Combines and formats the date and time nicely.
        """
        return f"{self.date.strftime('%b %d, %Y')} at {self.time.strftime('%I:%M %p')}"

    @classmethod
    def past_workouts(cls, user):
        """Retrieve past workouts for a specific user."""
        today = timezone.now().date()
        return cls.objects.filter(user=user, date__lt=today).order_by('-date')


class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="measurements")
    week = models.PositiveIntegerField()  # Week number
    year = models.PositiveIntegerField()
    weight = models.FloatField(blank=True, null=True)  # Optional fields
    chest = models.FloatField(blank=True, null=True)
    arm = models.FloatField(blank=True, null=True)
    waist = models.FloatField(blank=True, null=True)
    hips = models.FloatField(blank=True, null=True)
    thighs = models.FloatField(blank=True, null=True)
    calf = models.FloatField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Week {self.week}, {self.year} - {self.user.username}"
