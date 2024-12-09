from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Workout


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
    # Allows the logged-in user to create a new workout.
    model = Workout
    fields = ['name', 'exercises', 'duration', 'intensity']
    template_name = 'workouts/workout_form.html'
    success_url = reverse_lazy('workouts:list')

    def form_valid(self, form):
        # Assign the logged-in user as the workout creator.
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    # Allows the logged-in user to update an existing workout.
    model = Workout
    fields = ['name', 'exercises', 'duration', 'intensity']
    template_name = 'workouts/workout_form.html'
    success_url = reverse_lazy('workouts:list')


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    # Allows the logged-in user to delete a workout.
    model = Workout
    template_name = 'workouts/workout_confirm_delete.html'
    success_url = reverse_lazy('workouts:list')
