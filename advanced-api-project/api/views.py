from django.shortcuts import render
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorListSerializer


class BookListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all books.
    
    This view provides read-only access to all books and includes
    filtering, searching, and pagination capabilities.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow read access to everyone
    
    # Add filtering and searching capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['-publication_year', 'title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single book by ID.
    
    This view provides read-only access to individual book details
    and includes related author information.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow read access to everyone
    lookup_field = 'pk'


class BookCreateView(generics.CreateAPIView):
    """
    Generic CreateView for adding new books.
    
    This view handles book creation with proper validation and
    requires user authentication for security.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_create(self, serializer):
        """
        Custom method to handle book creation.
        
        This method can be extended to add custom logic during
        book creation, such as logging or additional validation.
        """
        book = serializer.save()
        # Log the creation (you can extend this with actual logging)
        print(f"New book created: {book.title} by {book.author.name}")
        return book


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView for modifying existing books.
    
    This view handles both partial and full updates of book
    information and requires user authentication.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        """
        Custom method to handle book updates.
        
        This method can be extended to add custom logic during
        book updates, such as change tracking or validation.
        """
        book = serializer.save()
        # Log the update (you can extend this with actual logging)
        print(f"Book updated: {book.title} by {book.author.name}")
        return book


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView for removing books.
    
    This view handles book deletion and requires user authentication
    for security. It also provides a custom response message.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    lookup_field = 'pk'
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to provide better response handling.
        
        This method captures the book information before deletion
        and returns a custom response message.
        """
        book = self.get_object()
        book_title = book.title
        book_author = book.author.name
        
        # Perform the deletion
        response = super().destroy(request, *args, **kwargs)
        
        # Custom response message
        response.data = {
            'message': f'Book "{book_title}" by {book_author} has been successfully deleted.',
            'deleted_book': {
                'title': book_title,
                'author': book_author
            }
        }
        return response


class BookListCreateView(generics.ListCreateAPIView):
    """
    Combined ListCreateView for books with conditional permissions.
    
    This view combines listing and creation in a single endpoint,
    with different permissions for different operations.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read for everyone, write for authenticated
    
    # Add filtering and searching capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['-publication_year', 'title']
    
    def get_permissions(self):
        """
        Custom permission handling based on the request method.
        
        This method provides different permissions for different
        HTTP methods to ensure proper access control.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined RetrieveUpdateDestroyView for comprehensive book management.
    
    This view provides a single endpoint for retrieving, updating,
    and deleting individual books with appropriate permissions.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read for everyone, write for authenticated
    lookup_field = 'pk'
    
    def get_permissions(self):
        """
        Custom permission handling based on the request method.
        
        This method provides different permissions for different
        HTTP methods to ensure proper access control.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


# Author views (keeping existing functionality)
class AuthorListCreateView(generics.ListCreateAPIView):
    """
    View for listing all authors and creating new authors.
    
    Uses AuthorListSerializer for listing to avoid performance issues
    with nested book serialization.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        """Custom permission handling based on request method."""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting individual authors.
    
    Uses AuthorSerializer to provide full author details including
    nested book information.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        """Custom permission handling based on request method."""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


@api_view(['GET'])
@permission_classes([AllowAny])
def test_serializers(request):
    """
    Test endpoint to demonstrate serializer functionality.
    
    This endpoint creates sample data and shows how the serializers
    handle nested relationships and validation.
    """
    # Create a test author if none exists
    author, created = Author.objects.get_or_create(
        name="J.R.R. Tolkien",
        defaults={'name': "J.R.R. Tolkien"}
    )
    
    # Create test books if none exist
    book1, created1 = Book.objects.get_or_create(
        title="The Hobbit",
        author=author,
        defaults={'publication_year': 1937}
    )
    
    book2, created2 = Book.objects.get_or_create(
        title="The Lord of the Rings",
        author=author,
        defaults={'publication_year': 1954}
    )
    
    # Test serialization
    author_serializer = AuthorSerializer(author)
    book_serializer = BookSerializer(book1)
    
    return Response({
        'message': 'Serializer test completed successfully',
        'author_data': author_serializer.data,
        'book_data': book_serializer.data,
        'created_objects': {
            'author_created': created,
            'book1_created': created1,
            'book2_created': created2
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    API information endpoint providing documentation and status.
    
    This endpoint returns basic information about the API including
    available endpoints and their purposes.
    """
    api_info = {
        "api_name": "Advanced API Project - Book Management System",
        "version": "1.0.0",
        "description": "A comprehensive API for managing authors and books with advanced serializers",
        "endpoints": {
            "books": {
                "list": "/api/books/",
                "detail": "/api/books/<id>/",
                "create": "/api/books/create/",
                "update": "/api/books/<id>/update/",
                "delete": "/api/books/<id>/delete/",
                "combined": "/api/books/combined/",
                "advanced": "/api/books/advanced/",
                "create_advanced": "/api/books/create-advanced/"
            },
            "authors": {
                "list": "/api/authors/",
                "detail": "/api/authors/<id>/"
            },
            "utility": {
                "test": "/api/test/",
                "info": "/api/info/"
            }
        },
        "features": [
            "Custom serializers with nested relationships",
            "Advanced filtering and searching",
            "Permission-based access control",
            "Generic views and ViewSets",
            "Custom validation and error handling"
        ]
    }
    return Response(api_info)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def book_update_general(request):
    """
    General book update endpoint that requires authentication.
    
    This endpoint demonstrates the permission system by requiring
    authentication for update operations.
    """
    return Response({
        "message": "Book update endpoint - authentication required",
        "status": "success",
        "permission": "authenticated_users_only"
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def book_delete_general(request):
    """
    General book delete endpoint that requires authentication.
    
    This endpoint demonstrates the permission system by requiring
    authentication for delete operations.
    """
    return Response({
        "message": "Book delete endpoint - authentication required",
        "status": "success",
        "permission": "authenticated_users_only"
    })


class SimpleTestView(generics.GenericAPIView):
    """
    Simple test view to verify permission system.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response({
            "message": "This endpoint requires authentication",
            "user": str(request.user),
            "authenticated": request.user.is_authenticated
        })
