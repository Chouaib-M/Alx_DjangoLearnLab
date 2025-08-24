from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Notification model.
    """
    list_display = ('recipient', 'actor', 'verb', 'timestamp', 'read')
    list_filter = ('read', 'timestamp', 'verb')
    search_fields = ('recipient__username', 'actor__username', 'verb')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    fieldsets = (
        (None, {
            'fields': ('recipient', 'actor', 'verb', 'read')
        }),
        ('Target', {
            'fields': ('target_content_type', 'target_object_id'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'actor')
