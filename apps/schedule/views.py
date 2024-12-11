from calendar import monthrange
from datetime import datetime, timedelta, date
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import WorkoutScheduleForm
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


def monthly_schedule_view(request):
    # Get the 'month_start' parameter from the request
    month_start_str = request.GET.get('month_start')
    if month_start_str:
        month_start = date.fromisoformat(month_start_str)
    else:
        today = now().date()
        month_start = date(today.year, today.month, 1)  # First day of the current month

    # Get the total number of days in the selected month
    _, num_days = monthrange(month_start.year, month_start.month)

    # Calculate the start and end dates of the month
    month_end = month_start.replace(day=num_days)

    # Fetch all schedules for the user within the month
    schedules = WorkoutSchedule.objects.filter(
        date__range=[month_start, month_end],
        user=request.user
    )

    # Organize schedules by day
    monthly_schedule = {day: [] for day in range(1, num_days + 1)}
    for schedule in schedules:
        monthly_schedule[schedule.date.day].append(schedule)

    return render(request, 'schedule/monthly_schedule.html', {
        'monthly_schedule': monthly_schedule,
        'current_month_start': month_start,
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
