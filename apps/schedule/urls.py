from django.urls import path
from .views import WorkoutScheduleCreateView, measurement_tracker_view, schedule_view, edit_workout_view, \
    delete_workout_view

app_name = 'schedule'

urlpatterns = [
    path('', schedule_view, name='schedule_list'),
    path('add/', WorkoutScheduleCreateView.as_view(), name='schedule_add'),
    path('tracker/', measurement_tracker_view, name='measurement_tracker'),
    path('workout/edit/<int:workout_id>/', edit_workout_view, name='edit_workout'),
    path('workout/delete/<int:workout_id>/', delete_workout_view, name='delete_workout'),

]
