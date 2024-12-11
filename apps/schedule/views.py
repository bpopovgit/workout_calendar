from datetime import datetime, timedelta
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


def weekly_schedule_view(request):
    from django.utils.timezone import now
    from datetime import timedelta, datetime
    from .models import WorkoutSchedule

    # Get the 'week_start' parameter from the request
    week_start_str = request.GET.get('week_start')
    if week_start_str:
        try:
            week_start = datetime.strptime(week_start_str, '%Y-%m-%d').date()
        except ValueError:
            week_start = now().date()
    else:
        week_start = now().date()

    # Calculate the week's Monday
    # Adjust for weeks that may start on different days (e.g., if the system uses Sunday as the first day of the week)
    weekday = week_start.weekday()  # 0 = Monday, 6 = Sunday
    monday = week_start - timedelta(days=weekday)

    # Calculate Sunday
    sunday = monday + timedelta(days=6)

    # Filter schedules for the selected week
    schedules = WorkoutSchedule.objects.filter(date__range=[monday, sunday], user=request.user)

    # Organize schedules by day
    weekly_schedule = {day: [] for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
    for schedule in schedules:
        weekday_name = schedule.date.strftime('%A')  # Get the name of the day
        weekly_schedule[weekday_name].append(schedule)

    return render(request, 'schedule/weekly_schedule.html', {
        'weekly_schedule': weekly_schedule,
        'current_week_start': monday,  # Pass the start of the current week
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
