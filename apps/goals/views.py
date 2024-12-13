import random

from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import WorkoutLog
from .forms import WorkoutLogForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Goal
from .forms import GoalForm


class WorkoutLogListView(LoginRequiredMixin, ListView):
    model = WorkoutLog
    template_name = 'goals/workout_log_list.html'
    context_object_name = 'workout_logs'

    def get_queryset(self):
        return WorkoutLog.objects.filter(user=self.request.user).order_by('-date_completed')


class WorkoutLogCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutLog
    form_class = WorkoutLogForm
    template_name = 'goals/workout_log_form.html'
    success_url = reverse_lazy('goals:log_list')

    def get_form_kwargs(self):
        # Pass the logged-in user to the form
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Assign the logged-in user to the WorkoutLog
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def create_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals:goal_list')  # Redirect to the Goals page
    else:
        form = GoalForm()
    return render(request, 'goals/create_goal.html', {'form': form})


@login_required
def edit_goal(request, pk):  # Updated function name
    goal = get_object_or_404(Goal, pk=pk, user=request.user)  # Use get_object_or_404 for better error handling
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goals:goal_list')  # Redirect to the Goals page
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/edit_goal.html', {'form': form})


@login_required
def goal_list_view(request):
    goals = Goal.objects.filter(user=request.user, is_active=True).order_by('-created_at')
    return render(request, 'goals/goal_list.html', {'goals': goals})


@login_required
def goal_list_view(request):
    quotes = [
        "Believe you can, and you're halfway there.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "The future belongs to those who believe in the beauty of their dreams.",
    ]
    selected_quote = random.choice(quotes)
    goals = Goal.objects.filter(user=request.user, is_active=True).order_by('-created_at')
    return render(request, 'goals/goal_list.html', {'goals': goals, 'quote': selected_quote})

@login_required
def delete_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == "POST":
        goal.delete()
        return HttpResponseRedirect(reverse('goals:goal_list'))
    return render(request, 'goals/delete_goal_confirm.html', {'goal': goal})
