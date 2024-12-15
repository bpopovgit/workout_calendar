from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import WorkoutForm
from .models import Workout
from ..goals.models import WorkoutLog
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.schedule.models import WorkoutSchedule


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
        """Filter only past workouts for the logged-in user."""
        return WorkoutSchedule.past_workouts(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_workouts'] = self.get_queryset().count()
        return context
