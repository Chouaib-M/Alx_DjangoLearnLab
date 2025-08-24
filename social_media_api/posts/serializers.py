from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model with author information and comment count.
    """
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.ReadOnlyField(source='author.id')
    comments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'author_id', 
            'comments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create a new post with the current user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostDetailSerializer(PostSerializer):
    """
    Detailed serializer for Post model including comments.
    """
    comments = serializers.SerializerMethodField()
    
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['comments']
    
    def get_comments(self, obj):
        """Get all comments for this post."""
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model with author information.
    """
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.ReadOnlyField(source='author.id')
    post_title = serializers.ReadOnlyField(source='post.title')
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'author_id', 'post', 
            'post_title', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create a new comment with the current user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating comments (simplified for nested creation).
    """
    class Meta:
        model = Comment
        fields = ['content']

    def create(self, validated_data):
        """Create a new comment with the current user as author and specified post."""
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = self.context['post']
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model.
    """
    user = serializers.StringRelatedField(read_only=True)
    post_title = serializers.ReadOnlyField(source='post.title')
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'post_title', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']
