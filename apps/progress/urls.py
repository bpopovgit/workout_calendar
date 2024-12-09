from django.urls import path
from .views import WorkoutLogListView, WorkoutLogCreateView

app_name = 'progress'

urlpatterns = [
    path('', WorkoutLogListView.as_view(), name='log_list'),
    path('add/', WorkoutLogCreateView.as_view(), name='log_add'),
]
