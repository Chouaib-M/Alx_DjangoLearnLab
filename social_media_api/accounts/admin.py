from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for CustomUser model.
    Extends Django's default UserAdmin to include custom fields.
    """
    # Fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'followers_count')
    
    # Add custom fields to the user form
    fieldsets = UserAdmin.fieldsets + (
        ('Social Media Info', {
            'fields': ('bio', 'profile_picture', 'followers')
        }),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Social Media Info', {
            'fields': ('bio', 'profile_picture')
        }),
    )
    
    # Configure the many-to-many field display
    filter_horizontal = ('followers',)
