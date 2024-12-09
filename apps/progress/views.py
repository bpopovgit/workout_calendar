from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import WorkoutLog
from .forms import WorkoutLogForm


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
