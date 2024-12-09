from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import WorkoutSchedule
from .forms import WorkoutScheduleForm


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
