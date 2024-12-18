from django.contrib import admin
from .models import WorkoutSchedule


@admin.register(WorkoutSchedule)
class WorkoutScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout', 'date', 'time', 'completed')
    search_fields = ('user__username', 'workout__name')
    list_filter = ('completed', 'date', 'time')
    readonly_fields = ('date', 'time')
