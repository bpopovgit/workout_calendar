from django.urls import path
from .views import (
    WorkoutListView,
    WorkoutDetailView,
    WorkoutCreateView,
    WorkoutUpdateView,
    WorkoutDeleteView,
    WorkoutHistoryView,
)
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', WorkoutListView.as_view(), name='list'),
    path('<int:pk>/', WorkoutDetailView.as_view(), name='detail'),
    path('create/', WorkoutCreateView.as_view(), name='create'),
    path('<int:pk>/update/', WorkoutUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', WorkoutDeleteView.as_view(), name='delete'),
    path('history/', WorkoutHistoryView.as_view(), name='workout_history'),
]
