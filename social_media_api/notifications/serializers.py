from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """
    actor = serializers.StringRelatedField(read_only=True)
    actor_id = serializers.ReadOnlyField(source='actor.id')
    target_type = serializers.SerializerMethodField()
    target_id = serializers.ReadOnlyField(source='target_object_id')
    
    class Meta:
        model = Notification
        fields = [
            'id', 'actor', 'actor_id', 'verb', 'target_type', 
            'target_id', 'timestamp', 'read'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_target_type(self, obj):
        """Get the content type name of the target object."""
        if obj.target_content_type:
            return obj.target_content_type.model
        return None


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating notification read status.
    """
    class Meta:
        model = Notification
        fields = ['read']
