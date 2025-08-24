from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Test cases for CustomUser model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """Test that user is created with custom fields."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.followers_count, 0)
        self.assertEqual(self.user.following_count, 0)
    
    def test_user_str_method(self):
        """Test string representation of user."""
        self.assertEqual(str(self.user), 'testuser')


class UserRegistrationTest(APITestCase):
    """Test cases for user registration."""
    
    def test_user_registration_success(self):
        """Test successful user registration."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post('/api/accounts/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
    
    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'differentpass',
        }
        response = self.client.post('/api/accounts/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(APITestCase):
    """Test cases for user login."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_login_success(self):
        """Test successful user login."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/accounts/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/accounts/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FollowAPITest(APITestCase):
    """Test cases for follow/unfollow functionality."""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
    
    def test_follow_user_success(self):
        """Test successfully following a user."""
        response = self.client.post(f'/api/accounts/follow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user1.is_following(self.user2))
        self.assertIn('following', response.data)
        self.assertTrue(response.data['following'])
    
    def test_follow_self_error(self):
        """Test that user cannot follow themselves."""
        response = self.client.post(f'/api/accounts/follow/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_follow_already_following_error(self):
        """Test error when trying to follow already followed user."""
        self.user1.follow(self.user2)
        response = self.client.post(f'/api/accounts/follow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already following', response.data['error'])
    
    def test_unfollow_user_success(self):
        """Test successfully unfollowing a user."""
        self.user1.follow(self.user2)
        response = self.client.post(f'/api/accounts/unfollow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user1.is_following(self.user2))
        self.assertFalse(response.data['following'])
    
    def test_unfollow_not_following_error(self):
        """Test error when trying to unfollow user not being followed."""
        response = self.client.post(f'/api/accounts/unfollow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('not following', response.data['error'])
    
    def test_follow_nonexistent_user(self):
        """Test following a non-existent user."""
        response = self.client.post('/api/accounts/follow/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
