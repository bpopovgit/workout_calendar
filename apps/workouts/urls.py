from django.urls import path
from .views import (
    WorkoutListView,
    WorkoutDetailView,
    WorkoutCreateView,
    WorkoutUpdateView,
    WorkoutDeleteView,
)

app_name = 'workouts'

urlpatterns = [
    path('', WorkoutListView.as_view(), name='list'),
    path('<int:pk>/', WorkoutDetailView.as_view(), name='detail'),
    path('create/', WorkoutCreateView.as_view(), name='create'),
    path('<int:pk>/update/', WorkoutUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', WorkoutDeleteView.as_view(), name='delete'),
]
