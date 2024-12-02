from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goal = models.CharField(
        max_length=100,
        choices=[
            ('Weight Loss', 'Weight Loss'),
            ('Muscle Gain', 'Muscle Gain'),
            ('Endurance', 'Endurance'),
        ]
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
