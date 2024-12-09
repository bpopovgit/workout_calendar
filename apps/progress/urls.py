from .views import WorkoutLogListView, WorkoutLogCreateView
from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', WorkoutLogListView.as_view(), name='log_list'),
    path('add/', WorkoutLogCreateView.as_view(), name='log_add'),
    path('create/', views.create_goal, name='create_goal'),
    path('<int:pk>/edit/', views.update_goal, name='update_goal'),
]
