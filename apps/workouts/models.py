from django.db import models
from django.contrib.auth.models import User


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    muscle_group = models.CharField(
        max_length=100,
        choices=[
            ('Upper Body', 'Upper Body'),
            ('Lower Body', 'Lower Body'),
            ('Cardio', 'Cardio'),
            ('Core', 'Core'),
        ]
    )

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    exercises = models.ManyToManyField(Exercise)
    duration = models.DurationField()  # e.g., 1 hour
    intensity = models.CharField(
        max_length=50,
        choices=[
            ('Low', 'Low'),
            ('Moderate', 'Moderate'),
            ('High', 'High'),
        ]
    )

    def __str__(self):
        return self.name
