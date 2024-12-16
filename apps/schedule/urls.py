from django.urls import path
from .views import WorkoutScheduleCreateView, schedule_view, edit_workout_view, \
    delete_workout_view, mark_workout_completed

app_name = 'schedule'

urlpatterns = [
    path('', schedule_view, name='schedule_list'),
    path('add/', WorkoutScheduleCreateView.as_view(), name='schedule_add'),
    path('workout/edit/<int:workout_id>/', edit_workout_view, name='edit_workout'),
    path('workout/delete/<int:workout_id>/', delete_workout_view, name='delete_workout'),
    path('mark-completed/<int:workout_id>/', mark_workout_completed, name='mark_workout_completed'),

]
