from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds bio, profile_picture, and followers fields for social media functionality.
    """
    bio = models.TextField(max_length=500, blank=True, help_text="User biography")
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        help_text="User profile picture"
    )
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='following',
        blank=True,
        help_text="Users who follow this user"
    )
    
    def __str__(self):
        return self.username
    
    @property
    def followers_count(self):
        """Return the number of followers."""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Return the number of users this user is following."""
        return self.following.count()
