from calendar import monthrange
from datetime import datetime, timedelta, date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import WorkoutScheduleForm, EditWorkoutScheduleForm
from .models import WorkoutSchedule
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Measurement
from .forms import MeasurementForm
from django.shortcuts import render
from datetime import datetime, timedelta
import calendar


@login_required
def schedule_view(request):
    user = request.user

    # Get month_start from query params, default to the current month
    month_start = request.GET.get('month_start', datetime.now().strftime('%Y-%m'))
    try:
        # Convert month_start to a valid date
        start_date = datetime.strptime(month_start + '-01', '%Y-%m-%d').date()
    except ValueError:
        # Default to the current month if the input is invalid
        start_date = datetime.now().replace(day=1).date()

    # Calculate the first and last days of the month
    _, num_days = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date.replace(day=num_days)

    # Fetch workouts scheduled for the month
    workouts = user.schedules.filter(date__range=[start_date, end_date])

    # Organize workouts by day
    monthly_schedule = {}
    for workout in workouts:
        day = workout.date.day
        if day not in monthly_schedule:
            monthly_schedule[day] = []
        monthly_schedule[day].append(workout)

    # Generate dropdown choices for the past 5 years and the next 5 years
    today = datetime.now()
    month_choices = [
        (today.replace(year=today.year + offset, month=month, day=1))
        for offset in range(-5, 6)  # From -5 years to +5 years
        for month in range(1, 13)
    ]

    context = {
        'current_month_start': start_date,  # Pass the correctly calculated start_date
        'monthly_schedule': monthly_schedule,
        'weeks': [
            [days for days in range(1, num_days + 1)][i: i + 7]
            for i in range(0, num_days, 7)
        ],
        'month_choices': month_choices,
    }
    return render(request, 'schedule/monthly_schedule.html', context)


class WorkoutScheduleCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSchedule
    form_class = WorkoutScheduleForm
    template_name = 'schedule/schedule_form.html'
    success_url = reverse_lazy('schedule:schedule_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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


@login_required
def edit_workout_view(request, workout_id):
    # Retrieve the workout or return 404 if not found
    workout = get_object_or_404(WorkoutSchedule, id=workout_id, user=request.user)

    if request.method == 'POST':
        # Handle form submission
        form = EditWorkoutScheduleForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Workout updated successfully!'})
        else:
            # Return form errors if invalid
            return JsonResponse({'status': 'error', 'errors': form.errors})

    # Handle GET request: Render the form and return it as part of the response
    form_html = render(request, 'schedule/edit_form.html', {
        'form': EditWorkoutScheduleForm(instance=workout),
    }).content.decode()

    return JsonResponse({'status': 'success', 'form': form_html})


@login_required
def delete_workout_view(request, workout_id):
    workout = get_object_or_404(WorkoutSchedule, id=workout_id, user=request.user)
    if request.method == 'POST':
        workout.delete()
        return JsonResponse({'status': 'success', 'message': 'Workout deleted successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
