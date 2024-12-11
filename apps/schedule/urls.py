from django.urls import path
from .views import WorkoutScheduleCreateView, measurement_tracker_view, schedule_view

app_name = 'schedule'

urlpatterns = [
    path('', schedule_view, name='schedule_list'),
    path('add/', WorkoutScheduleCreateView.as_view(), name='schedule_add'),
    path('tracker/', measurement_tracker_view, name='measurement_tracker'),

]
