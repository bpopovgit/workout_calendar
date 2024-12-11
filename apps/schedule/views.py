from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import WorkoutSchedule
from .forms import WorkoutScheduleForm
from django.shortcuts import render
from django.utils.timezone import now, timedelta
from .models import WorkoutSchedule
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import Measurement
from .forms import MeasurementForm


class WorkoutScheduleListView(LoginRequiredMixin, ListView):
    model = WorkoutSchedule
    template_name = 'schedule/schedule_list.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        return WorkoutSchedule.objects.filter(user=self.request.user).order_by('date', 'time')


class WorkoutScheduleCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSchedule
    form_class = WorkoutScheduleForm
    template_name = 'schedule/schedule_form.html'
    success_url = reverse_lazy('schedule:schedule_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def weekly_schedule_view(request):
    user = request.user
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    # Query workouts for the week
    week_workouts = WorkoutSchedule.objects.filter(
        user=user, date__range=[start_of_week, end_of_week]
    ).order_by('date', 'time')

    # Organize workouts by day
    weekly_schedule = {start_of_week + timedelta(days=i): [] for i in range(7)}
    for workout in week_workouts:
        weekly_schedule[workout.date].append(workout)

    return render(request, 'schedule/weekly_schedule.html', {
        'weekly_schedule': weekly_schedule,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
    })


def measurement_tracker_view(request):
    user = request.user
    today = now()
    week_number = today.isocalendar()[1]
    year = today.year

    # Get or create the measurement for the current week
    measurement, created = Measurement.objects.get_or_create(
        user=user, week=week_number, year=year
    )

    if request.method == 'POST':
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            return redirect('schedule:measurement_tracker')
    else:
        form = MeasurementForm(instance=measurement)

    return render(request, 'schedule/measurement_tracker.html', {'form': form})
