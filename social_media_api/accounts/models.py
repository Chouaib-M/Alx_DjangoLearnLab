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
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
        help_text="Users this user is following"
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
    
    def follow(self, user):
        """Follow a user."""
        if user != self:
            self.following.add(user)
    
    def unfollow(self, user):
        """Unfollow a user."""
        self.following.remove(user)
    
    def is_following(self, user):
        """Check if this user is following another user."""
        return self.following.filter(id=user.id).exists()
