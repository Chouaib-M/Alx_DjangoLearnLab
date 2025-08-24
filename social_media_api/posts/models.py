from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """
    Post model for social media posts.
    """
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        help_text="The user who created this post"
    )
    title = models.CharField(
        max_length=200, 
        help_text="Title of the post"
    )
    content = models.TextField()  # Content/body of the post
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the post was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the post was last updated"
    )

    class Meta:
        ordering = ['-created_at']  # Show newest posts first
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    @property
    def comments_count(self):
        """Return the number of comments on this post."""
        return self.comments.count()


class Comment(models.Model):
    """
    Comment model for comments on posts.
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text="The post this comment belongs to"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text="The user who created this comment"
    )
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the comment was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the comment was last updated"
    )

    class Meta:
        ordering = ['created_at']  # Show oldest comments first
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
