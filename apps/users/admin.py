from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)  # Keep UserProfile inline

    def get_fieldsets(self, request, obj=None):
        """
        Restrict 'Permissions' to superusers while retaining UserProfile.
        """
        if not request.user.is_superuser:
            return (
                (None, {'fields': ('username', 'password')}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
                ('Profile', {'fields': ('userprofile__goal', 'userprofile__profile_picture')}),
                # Include Profile fields
                ('Important dates', {'fields': ('last_login', 'date_joined')}),
            )
        return super().get_fieldsets(request, obj)

    def has_delete_permission(self, request, obj=None):
        """
        Restrict user deletion to superusers.
        """
        return request.user.is_superuser


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'phone_number', 'created_at')
    search_fields = ('user__username', 'goal', 'phone_number')
    list_filter = ('goal', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
