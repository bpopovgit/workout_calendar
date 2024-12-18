from django.contrib import admin
from .models import Exercise, Workout


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_group')
    search_fields = ('name', 'muscle_group')
    list_filter = ('muscle_group',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'intensity', 'duration')
    search_fields = ('name', 'user__username')
    list_filter = ('intensity', 'duration')
    filter_horizontal = ('exercises',)  # Allows selection of multiple exercises
