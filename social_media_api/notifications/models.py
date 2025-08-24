from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Notification(models.Model):
    """
    Notification model for user notifications.
    Uses GenericForeignKey to reference any model as the target.
    """
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who receives the notification"
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        help_text="User who performed the action"
    )
    verb = models.CharField(
        max_length=255,
        help_text="Description of the action performed"
    )
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False, help_text="Whether notification has been read")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return f"{self.actor.username} {self.verb}"
    
    def mark_as_read(self):
        """Mark this notification as read."""
        self.read = True
        self.save()
