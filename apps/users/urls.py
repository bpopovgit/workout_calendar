from django.urls import path
from . import views
from .views import UserProfileUpdateView, SignUpView, user_profile_view, edit_profile, email_verify

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify-email/<uidb64>/<token>/', email_verify, name='email_verify'),
    path('profile/', user_profile_view, name='profile'),
    path('get_workout_data/', views.get_workout_data, name='get_workout_data'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('edit-profile/', edit_profile, name='edit_profile'),


]
