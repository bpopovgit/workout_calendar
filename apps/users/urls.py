from django.urls import path
from .views import UserProfileDetailView, UserProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('profile/', UserProfileDetailView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
]
