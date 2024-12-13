from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.public.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  # Home page
    path('admin/', admin.site.urls),  # Admin site
    path('users/', include('apps.users.urls')),  # Users app
    path('workouts/', include('apps.workouts.urls')),  # Workouts app
    path('schedule/', include('apps.schedule.urls')),  # Schedule app
    path('goals/', include('apps.goals.urls')),  # Progress app
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs

]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
