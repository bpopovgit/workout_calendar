from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile Fields
    goal = models.CharField(
        max_length=100,
        choices=[
            ('Weight Loss', 'Weight Loss'),
            ('Muscle Gain', 'Muscle Gain'),
            ('Endurance', 'Endurance'),
        ],
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        default='profile_pics/default.png'
    )
    bio = models.TextField(blank=True, null=True, help_text="Write something about yourself.")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Optional phone number")

    # Automatically updated timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
