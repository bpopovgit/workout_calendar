from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import WorkoutLog
from .forms import WorkoutLogForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Goal
from .forms import GoalForm


class WorkoutLogListView(LoginRequiredMixin, ListView):
    model = WorkoutLog
    template_name = 'progress/workout_log_list.html'
    context_object_name = 'workout_logs'

    def get_queryset(self):
        return WorkoutLog.objects.filter(user=self.request.user).order_by('-date_completed')


class WorkoutLogCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutLog
    form_class = WorkoutLogForm
    template_name = 'progress/workout_log_form.html'
    success_url = reverse_lazy('progress:log_list')

    def form_valid(self, form):
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
            return redirect('profile')  # Redirect to profile page
    else:
        form = GoalForm()
    return render(request, 'progress/create_goal.html', {'form': form})


@login_required
def update_goal(request, pk):
    goal = Goal.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'progress/update_goal.html', {'form': form})
