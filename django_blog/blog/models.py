from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    """
    Blog Post model for managing blog posts with CRUD operations.
    This model supports the blog post management features including:
    - Creating new posts (authenticated users only)
    - Reading posts (all users)
    - Updating posts (author only via LoginRequiredMixin and UserPassesTestMixin)
    - Deleting posts (author only via LoginRequiredMixin and UserPassesTestMixin)
    """
    title = models.CharField(max_length=200, help_text="Title of the blog post")
    content = models.TextField(help_text="Main content of the blog post")
    published_date = models.DateTimeField(auto_now_add=True, help_text="Date and time when post was created")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', 
                              help_text="Author of the post - used for permission checks")

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
