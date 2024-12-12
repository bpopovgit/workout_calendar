from django.urls import path
from . import views
from .views import UserProfileUpdateView, SignUpView, user_profile_view

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', user_profile_view, name='profile'),
    path('get_workout_data/', views.get_workout_data, name='get_workout_data'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),


]
