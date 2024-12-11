from django.urls import path
from .views import WorkoutScheduleListView, WorkoutScheduleCreateView, weekly_schedule_view, measurement_tracker_view

app_name = 'schedule'

urlpatterns = [
    path('', WorkoutScheduleListView.as_view(), name='schedule_list'),
    path('add/', WorkoutScheduleCreateView.as_view(), name='schedule_add'),
    path('weekly/', weekly_schedule_view, name='weekly_schedule'),
    path('tracker/', measurement_tracker_view, name='measurement_tracker'),

]
