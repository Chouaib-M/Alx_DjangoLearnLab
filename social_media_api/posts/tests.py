from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Post, Comment

User = get_user_model()


class PostModelTest(TestCase):
    """Test cases for Post model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )
    
    def test_post_creation(self):
        """Test that post is created correctly."""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.comments_count, 0)
    
    def test_post_str_method(self):
        """Test string representation of post."""
        expected = f"Test Post by {self.user.username}"
        self.assertEqual(str(self.post), expected)


class CommentModelTest(TestCase):
    """Test cases for Comment model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )
        self.comment = Comment.objects.create(
            content='This is a test comment.',
            author=self.user,
            post=self.post
        )
    
    def test_comment_creation(self):
        """Test that comment is created correctly."""
        self.assertEqual(self.comment.content, 'This is a test comment.')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)
    
    def test_comment_str_method(self):
        """Test string representation of comment."""
        expected = f"Comment by {self.user.username} on {self.post.title}"
        self.assertEqual(str(self.comment), expected)


class PostAPITest(APITestCase):
    """Test cases for Post API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.'
        }
    
    def test_create_post(self):
        """Test creating a new post."""
        response = self.client.post('/api/posts/', self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)
    
    def test_list_posts(self):
        """Test listing posts."""
        Post.objects.create(title='Test Post', content='Content', author=self.user)
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_post(self):
        """Test retrieving a specific post."""
        post = Post.objects.create(title='Test Post', content='Content', author=self.user)
        response = self.client.get(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')
    
    def test_update_own_post(self):
        """Test updating own post."""
        post = Post.objects.create(title='Test Post', content='Content', author=self.user)
        update_data = {'title': 'Updated Post', 'content': 'Updated content'}
        response = self.client.put(f'/api/posts/{post.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Post')
    
    def test_delete_own_post(self):
        """Test deleting own post."""
        post = Post.objects.create(title='Test Post', content='Content', author=self.user)
        response = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)


class CommentAPITest(APITestCase):
    """Test cases for Comment API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )
        
        self.comment_data = {
            'content': 'This is a test comment.',
            'post': self.post.id
        }
    
    def test_create_comment(self):
        """Test creating a new comment."""
        response = self.client.post('/api/comments/', self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.user)
    
    def test_list_comments(self):
        """Test listing comments."""
        Comment.objects.create(content='Test comment', author=self.user, post=self.post)
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class FeedAPITest(APITestCase):
    """Test cases for Feed functionality."""
    
    def setUp(self):
        # Create users
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
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpass123'
        )
        
        # Create tokens
        self.token1 = Token.objects.create(user=self.user1)
        
        # User1 follows User2
        self.user1.follow(self.user2)
        
        # Create posts
        self.post1 = Post.objects.create(
            title='Post by User2',
            content='This is a post by user2',
            author=self.user2
        )
        self.post2 = Post.objects.create(
            title='Post by User3',
            content='This is a post by user3',
            author=self.user3
        )
    
    def test_feed_shows_followed_users_posts(self):
        """Test that feed shows posts from followed users only."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should contain post from user2 (followed) but not user3 (not followed)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.post_by_followed.id)
    
    def test_feed_empty_when_not_following_anyone(self):
        """Test that feed is empty when user doesn't follow anyone."""
        # Create a new user who doesn't follow anyone
        user4 = User.objects.create_user(
            username='user4',
            email='user4@example.com',
            password='testpass123'
        )
        token4 = Token.objects.create(user=user4)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token4.key)
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
