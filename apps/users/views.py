from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import UserProfile


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        # Return the UserProfile for the currently logged-in user
        return UserProfile.objects.get(user=self.request.user)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    # Allows the logged-in user to update their profile.
    model = UserProfile
    fields = ['goal', 'profile_picture']
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        # Return the UserProfile for the currently logged-in user
        return UserProfile.objects.get(user=self.request.user)
