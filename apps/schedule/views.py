from calendar import monthrange
from datetime import datetime, timedelta, date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
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
        start_date = datetime.strptime(month_start + '-01', '%Y-%m-%d').date()
    except ValueError:
        start_date = datetime.now().replace(day=1).date()

    _, num_days = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date.replace(day=num_days)

    # Fetch only the schedules for the logged-in user
    workouts = user.schedules.filter(date__range=[start_date, end_date])

    monthly_schedule = {}
    for workout in workouts:
        day = workout.date.day
        if day not in monthly_schedule:
            monthly_schedule[day] = []
        monthly_schedule[day].append(workout)

    # Correctly align the first day of the month to the appropriate weekday
    first_day_of_month = start_date.weekday()  # 0 = Monday, 6 = Sunday
    total_days = list(range(1, num_days + 1))
    padded_days = [None] * first_day_of_month + total_days  # Add padding for days before 1st
    weeks = [padded_days[i:i + 7] for i in range(0, len(padded_days), 7)]  # Split into weeks

    today = datetime.now()
    month_choices = [
        today.replace(year=today.year + offset, month=month, day=1)
        for offset in range(-5, 6)
        for month in range(1, 13)
    ]

    context = {
        'current_month_start': start_date,
        'monthly_schedule': monthly_schedule,
        'weeks': weeks,  # Pass corrected weeks to template
        'month_choices': month_choices,
    }
    return render(request, 'schedule/monthly_schedule.html', context)


class WorkoutScheduleCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSchedule
    form_class = WorkoutScheduleForm
    template_name = 'schedule/schedule_form.html'
    success_url = reverse_lazy('schedule:schedule_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the logged-in user to the form
        return kwargs

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
    """
    View to handle editing of a scheduled workout via AJAX.
    """
    workout = get_object_or_404(WorkoutSchedule, id=workout_id, user=request.user)

    if request.method == 'POST':
        form = EditWorkoutScheduleForm(request.POST, instance=workout, user=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Workout updated successfully!'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    # Render the form as HTML and return it to the client
    form_html = render_to_string(
        'schedule/edit_form.html',
        {'form': EditWorkoutScheduleForm(instance=workout, user=request.user)}
    )
    return JsonResponse({'status': 'success', 'form': form_html})



@login_required
def delete_workout_view(request, workout_id):
    workout = get_object_or_404(WorkoutSchedule, id=workout_id, user=request.user)
    if request.method == 'POST':
        workout.delete()
        return JsonResponse({'status': 'success', 'message': 'Workout deleted successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@login_required
@require_POST
def mark_workout_completed(request, workout_id):
    workout = get_object_or_404(WorkoutSchedule, id=workout_id, user=request.user)
    workout.completed = True
    workout.save()
    return JsonResponse({'status': 'success', 'message': 'Workout marked as completed.'})
