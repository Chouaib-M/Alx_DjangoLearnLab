from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import (
    PostSerializer, 
    PostDetailSerializer, 
    CommentSerializer,
    CommentCreateSerializer
)
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts with full CRUD operations.
    Includes filtering, searching, and pagination.
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'created_at']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """Set the author to the current user when creating a post."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific post."""
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a specific post."""
        post = self.get_object()
        serializer = CommentCreateSerializer(
            data=request.data, 
            context={'request': request, 'post': post}
        )
        if serializer.is_valid():
            comment = serializer.save()
            response_serializer = CommentSerializer(comment, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments with full CRUD operations.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'post', 'created_at']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        """Set the author to the current user when creating a comment."""
        serializer.save(author=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed_view(request):
    """
    Return posts from users that the current user follows.
    Posts are ordered by creation date (most recent first).
    """
    current_user = request.user
    
    # Get users that the current user is following
    following_users = current_user.following.all()
    
    # Get posts from followed users, ordered by creation date
    feed_posts = Post.objects.filter(
        author__in=following_users
    ).order_by('-created_at')
    
    # Apply pagination
    from rest_framework.pagination import PageNumberPagination
    paginator = PageNumberPagination()
    paginator.page_size = 10
    
    page = paginator.paginate_queryset(feed_posts, request)
    if page is not None:
        serializer = PostSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    serializer = PostSerializer(feed_posts, many=True, context={'request': request})
    return Response(serializer.data)
