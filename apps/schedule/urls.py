from django.urls import path
from .views import WorkoutScheduleListView, WorkoutScheduleCreateView

app_name = 'schedule'

urlpatterns = [
    path('', WorkoutScheduleListView.as_view(), name='schedule_list'),
    path('add/', WorkoutScheduleCreateView.as_view(), name='schedule_add'),
]
