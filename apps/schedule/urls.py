from django.urls import path
from .views import WorkoutScheduleListView, WorkoutScheduleCreateView, measurement_tracker_view, \
    monthly_schedule_view

app_name = 'schedule'

urlpatterns = [
    path('', WorkoutScheduleListView.as_view(), name='schedule_list'),
    path('add/', WorkoutScheduleCreateView.as_view(), name='schedule_add'),
    path('monthly/', monthly_schedule_view, name='monthly_schedule'),
    path('tracker/', measurement_tracker_view, name='measurement_tracker'),

]
