from django.urls import path
from .views import UserProfileDetailView, UserProfileUpdateView, SignUpView

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', UserProfileDetailView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
]
