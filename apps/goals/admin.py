from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'due_date', 'progress', 'get_percentage_complete')
    search_fields = ('name', 'user__username')
    list_filter = ('due_date',)  # Removed 'percentage_complete' from filters, as it is a calculated property.

    def get_percentage_complete(self, obj):
        """Return the calculated percentage complete."""
        return f"{obj.percentage_complete:.0f}%"

    get_percentage_complete.short_description = 'Percentage Complete'
