from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer


class NotificationListView(generics.ListAPIView):
    """
    View to list all notifications for the authenticated user.
    Shows unread notifications first.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        """Get notifications for the current user, unread first."""
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('read', '-timestamp')


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve and update a specific notification.
    Users can only access their own notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get notifications for the current user only."""
        return Notification.objects.filter(recipient=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializer for updates."""
        if self.request.method in ['PUT', 'PATCH']:
            return NotificationUpdateSerializer
        return NotificationSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    """
    Mark a specific notification as read.
    """
    notification = get_object_or_404(
        Notification, 
        pk=pk, 
        recipient=request.user
    )
    
    notification.mark_as_read()
    
    return Response(
        {'message': 'Notification marked as read'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """
    Mark all notifications as read for the authenticated user.
    """
    updated_count = Notification.objects.filter(
        recipient=request.user,
        read=False
    ).update(read=True)
    
    return Response(
        {
            'message': f'{updated_count} notifications marked as read',
            'updated_count': updated_count
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_notifications_count(request):
    """
    Get the count of unread notifications for the authenticated user.
    """
    count = Notification.objects.filter(
        recipient=request.user,
        read=False
    ).count()
    
    return Response(
        {'unread_count': count},
        status=status.HTTP_200_OK
    )
