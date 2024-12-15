from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .forms import WorkoutForm
from .models import Workout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from reportlab.pdfgen import canvas
import csv
from apps.schedule.models import WorkoutSchedule
from django.views.generic import ListView


class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts/workout_list.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        # Only show workouts created by the logged-in user
        return Workout.objects.filter(user=self.request.user)


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    # Displays the details of a specific workout.
    model = Workout
    template_name = 'workouts/workout_detail.html'
    context_object_name = 'workout'


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = WorkoutForm  # Use the custom form here
    template_name = 'workouts/workout_form.html'
    success_url = reverse_lazy('workouts:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'workouts/workout_form.html'
    success_url = reverse_lazy('workouts:list')


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    # Allows the logged-in user to delete a workout.
    model = Workout
    template_name = 'workouts/workout_confirm_delete.html'
    success_url = reverse_lazy('workouts:list')


class WorkoutHistoryView(LoginRequiredMixin, ListView):
    model = WorkoutSchedule
    template_name = "workouts/workout_history.html"
    context_object_name = "workouts"
    paginate_by = 10  # Show 10 workouts per page

    def get_queryset(self):
        """
        Filter past workouts for the logged-in user and apply search/filters.
        """
        user = self.request.user
        queryset = WorkoutSchedule.objects.filter(user=user, date__lt=timezone.now().date())

        # Filters
        intensity = self.request.GET.get('intensity')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search = self.request.GET.get('search')

        # Filtering on related Workout's intensity
        if intensity:
            queryset = queryset.filter(workout__intensity=intensity)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if search:
            queryset = queryset.filter(
                Q(workout__name__icontains=search) | Q(description__icontains=search)
            )

        return queryset.order_by('-date')

    def get(self, request, *args, **kwargs):
        """
        Handle export requests separately from the main ListView logic.
        """
        export_type = request.GET.get('export')
        if export_type:
            queryset = self.get_queryset()
            if export_type == 'csv':
                return self.export_as_csv(queryset)
            elif export_type == 'pdf':
                return self.export_as_pdf(queryset)
        return super().get(request, *args, **kwargs)

    def export_as_csv(self, queryset):
        """
        Export workout data as CSV.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="workout_history.csv"'
        writer = csv.writer(response)
        writer.writerow(['Workout Name', 'Date', 'Time', 'Intensity', 'Description'])
        for workout in queryset:
            writer.writerow([
                workout.workout.name,
                workout.date,
                workout.time,
                workout.workout.intensity,  # Use the related Workout intensity
                workout.description or 'N/A'
            ])
        return response

    def export_as_pdf(self, queryset):
        """
        Export workout data as PDF.
        """
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="workout_history.pdf"'
        p = canvas.Canvas(response)
        p.drawString(100, 800, "Workout History")
        y = 780
        for workout in queryset:
            p.drawString(100, y, f"{workout.workout.name} - {workout.date} - {workout.time} - {workout.workout.intensity}")
            y -= 20
            if y < 50:  # Create a new page if needed
                p.showPage()
                y = 800
        p.showPage()
        p.save()
        return response

    def get_context_data(self, **kwargs):
        """
        Add context for filters, search, pagination, monthly trends, and achievements.
        """
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Add total workouts count
        context['total_workouts'] = queryset.count()

        # Monthly Trends Data for Chart.js
        monthly_data = (
            queryset.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        context['monthly_data'] = {
            'labels': [entry['month'].strftime('%B %Y') for entry in monthly_data],
            'data': [entry['count'] for entry in monthly_data]
        }

        # Achievements
        achievements = []
        if context['total_workouts'] >= 50:
            achievements.append("You completed 50 workouts!")
        total_hours = sum([workout.workout.duration.total_seconds() / 3600 for workout in queryset if workout.workout.duration])
        if total_hours >= 10:
            achievements.append("You've logged 10 hours of workouts this month!")
        context['achievements'] = achievements

        return context
