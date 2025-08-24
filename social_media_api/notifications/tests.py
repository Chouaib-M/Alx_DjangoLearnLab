from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.contenttypes.models import ContentType

from .models import Notification
from posts.models import Post, Like

User = get_user_model()


class NotificationModelTest(TestCase):
    """Test cases for Notification model."""
    
    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user1)
    
    def test_notification_creation(self):
        """Test creating a notification."""
        notification = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(self.post),
            target_object_id=self.post.id
        )
        
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.actor, self.user2)
        self.assertEqual(notification.verb, 'liked your post')
        self.assertEqual(notification.target, self.post)
        self.assertFalse(notification.read)
    
    def test_mark_as_read(self):
        """Test marking notification as read."""
        notification = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='followed you'
        )
        
        self.assertFalse(notification.read)
        notification.mark_as_read()
        self.assertTrue(notification.read)


class NotificationAPITest(APITestCase):
    """Test cases for Notification API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user1)
        
        # Create test notifications
        self.notification1 = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(self.post),
            target_object_id=self.post.id
        )
        
        self.notification2 = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='started following you',
            read=True
        )
        
        self.client = APIClient()
    
    def test_list_notifications(self):
        """Test listing user's notifications."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.get('/api/notifications/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Unread notifications should come first
        self.assertFalse(response.data['results'][0]['read'])
        self.assertTrue(response.data['results'][1]['read'])
    
    def test_notification_detail(self):
        """Test retrieving a specific notification."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.get(f'/api/notifications/{self.notification1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.notification1.id)
        self.assertEqual(response.data['verb'], 'liked your post')
    
    def test_mark_notification_read(self):
        """Test marking a notification as read."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.post(f'/api/notifications/{self.notification1.id}/read/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.read)
    
    def test_mark_all_notifications_read(self):
        """Test marking all notifications as read."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.post('/api/notifications/mark-all-read/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 1)  # Only 1 unread notification
        
        # Verify all notifications are now read
        unread_count = Notification.objects.filter(recipient=self.user1, read=False).count()
        self.assertEqual(unread_count, 0)
    
    def test_unread_notifications_count(self):
        """Test getting unread notifications count."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.get('/api/notifications/unread-count/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)
    
    def test_notification_privacy(self):
        """Test that users can only see their own notifications."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.get('/api/notifications/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  # user2 has no notifications
    
    def test_notification_requires_authentication(self):
        """Test that notification endpoints require authentication."""
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NotificationIntegrationTest(APITestCase):
    """Test notification creation during user interactions."""
    
    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user1)
        
        self.client = APIClient()
    
    def test_like_creates_notification(self):
        """Test that liking a post creates a notification."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check notification was created
        notification = Notification.objects.filter(
            recipient=self.user1,
            actor=self.user2,
            verb='liked your post'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.target, self.post)
    
    def test_follow_creates_notification(self):
        """Test that following a user creates a notification."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.post(f'/api/accounts/follow/{self.user1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check notification was created
        notification = Notification.objects.filter(
            recipient=self.user1,
            actor=self.user2,
            verb='started following you'
        ).first()
        
        self.assertIsNotNone(notification)
    
    def test_comment_creates_notification(self):
        """Test that commenting on a post creates a notification."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.post(
            f'/api/posts/{self.post.id}/add_comment/',
            {'content': 'Great post!'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check notification was created
        notification = Notification.objects.filter(
            recipient=self.user1,
            actor=self.user2,
            verb='commented on your post'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.target, self.post)
    
    def test_self_actions_dont_create_notifications(self):
        """Test that users don't get notifications for their own actions."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        
        # Like own post
        self.client.post(f'/api/posts/{self.post.id}/like/')
        
        # Comment on own post
        self.client.post(
            f'/api/posts/{self.post.id}/add_comment/',
            {'content': 'My own comment'}
        )
        
        # Should have no notifications
        notification_count = Notification.objects.filter(recipient=self.user1).count()
        self.assertEqual(notification_count, 0)
