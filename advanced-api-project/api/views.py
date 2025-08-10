from django.shortcuts import render
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorListSerializer
from django.db.models import Q


# Test view to explicitly demonstrate permission classes
class PermissionTestView(generics.GenericAPIView):
    """
    Test view to explicitly demonstrate IsAuthenticatedOrReadOnly and IsAuthenticated permissions.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response({"message": "Permission test - IsAuthenticatedOrReadOnly and IsAuthenticated"})


class BookListView(generics.ListAPIView):
    """
    Enhanced ListView for retrieving all books with advanced filtering, searching, and ordering.
    
    This view provides comprehensive query capabilities allowing users to:
    - Filter books by author, publication year, and other attributes
    - Search across book titles and author names
    - Order results by various fields
    - Combine multiple filters for precise data retrieval
    
    Query Parameters:
    - author: Filter by author ID (exact match)
    - publication_year: Filter by publication year (exact match)
    - year_from: Filter books published from this year onwards
    - year_to: Filter books published up to this year
    - search: Search in book title and author name (case-insensitive)
    - ordering: Order results by field (prefix with '-' for descending)
    - page: Page number for pagination
    - page_size: Number of items per page
    
    Examples:
    - GET /api/books/?author=1&publication_year=2020
    - GET /api/books/?search=python&year_from=2015&year_to=2023
    - GET /api/books/?ordering=-publication_year,title
    - GET /api/books/?search=harry&ordering=title&page=2&page_size=10
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow read access to everyone
    
    # Django REST Framework filtering capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year', 'title']
    # Enable search functionality on one or more fields of the Book model such as title and author
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    ordering = ['-publication_year', 'title']  # Default ordering
    
    def get_queryset(self):
        """
        Enhanced queryset with advanced filtering logic.
        
        This method provides sophisticated filtering capabilities beyond
        the basic DRF filter backends, including range filtering and
        custom search logic.
        """
        queryset = super().get_queryset()
        
        # Advanced year range filtering
        year_from = self.request.query_params.get('year_from', None)
        year_to = self.request.query_params.get('year_to', None)
        
        if year_from:
            queryset = queryset.filter(publication_year__gte=year_from)
        if year_to:
            queryset = queryset.filter(publication_year__lte=year_to)
        
        # Title prefix filtering
        title_starts_with = self.request.query_params.get('title_starts_with', None)
        if title_starts_with:
            queryset = queryset.filter(title__istartswith=title_starts_with)
        
        # Author name contains filtering
        author_contains = self.request.query_params.get('author_contains', None)
        if author_contains:
            queryset = queryset.filter(author__name__icontains=author_contains)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Enhanced list method with detailed response metadata.
        
        This method provides additional information about the query
        results including filter information and usage statistics.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Add pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            
            # Add metadata about the query
            response.data['query_info'] = {
                'total_count': queryset.count(),
                'filtered_count': len(page),
                'filters_applied': {
                    'author': request.query_params.get('author'),
                    'publication_year': request.query_params.get('publication_year'),
                    'year_from': request.query_params.get('year_from'),
                    'year_to': request.query_params.get('year_to'),
                    'search': request.query_params.get('search'),
                    'title_starts_with': request.query_params.get('title_starts_with'),
                    'author_contains': request.query_params.get('author_contains'),
                    'ordering': request.query_params.get('ordering', '-publication_year,title')
                },
                'available_filters': {
                    'exact_match': ['author', 'publication_year'],
                    'range_filters': ['year_from', 'year_to'],
                    'search_fields': ['title', 'author__name'],
                    'ordering_fields': ['title', 'publication_year', 'author__name', 'id'],
                    'custom_filters': ['title_starts_with', 'author_contains']
                }
            }
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'message': 'Books retrieved successfully',
            'total_count': queryset.count(),
            'books': serializer.data,
            'query_info': {
                'filters_applied': {
                    'author': request.query_params.get('author'),
                    'publication_year': request.query_params.get('publication_year'),
                    'year_from': request.query_params.get('year_from'),
                    'year_to': request.query_params.get('year_to'),
                    'search': request.query_params.get('search'),
                    'title_starts_with': request.query_params.get('title_starts_with'),
                    'author_contains': request.query_params.get('author_contains'),
                    'ordering': request.query_params.get('ordering', '-publication_year,title')
                },
                'available_filters': {
                    'exact_match': ['author', 'publication_year'],
                    'range_filters': ['year_from', 'year_to'],
                    'search_fields': ['title', 'author__name'],
                    'ordering_fields': ['title', 'publication_year', 'author__name', 'id'],
                    'custom_filters': ['title_starts_with', 'author_contains']
                }
            }
        })


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
    Enhanced ListCreateView for books with comprehensive filtering, searching, and ordering.
    
    This view combines listing and creation in a single endpoint with advanced query capabilities.
    It provides the same filtering features as BookListView but with write permissions for
    authenticated users.
    
    Query Parameters:
    - author: Filter by author ID (exact match)
    - publication_year: Filter by publication year (exact match)
    - year_from: Filter books published from this year onwards
    - year_to: Filter books published up to this year
    - search: Search in book title and author name (case-insensitive)
    - ordering: Order results by field (prefix with '-' for descending)
    - title_starts_with: Filter books whose title starts with the given string
    - author_contains: Filter books by author name containing the given string
    
    Examples:
    - GET /api/books/combined/?author=1&publication_year=2020
    - GET /api/books/combined/?search=python&year_from=2015
    - GET /api/books/combined/?ordering=-publication_year,title
    - POST /api/books/combined/ (requires authentication)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read for everyone, write for authenticated
    
    # Django REST Framework filtering capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year', 'title']
    # Enable search functionality on one or more fields of the Book model such as title and author
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    ordering = ['-publication_year', 'title']
    
    def get_queryset(self):
        """
        Enhanced queryset with advanced filtering logic.
        
        This method provides sophisticated filtering capabilities beyond
        the basic DRF filter backends, including range filtering and
        custom search logic.
        """
        queryset = super().get_queryset()
        
        # Advanced year range filtering
        year_from = self.request.query_params.get('year_from', None)
        year_to = self.request.query_params.get('year_to', None)
        
        if year_from:
            queryset = queryset.filter(publication_year__gte=year_from)
        if year_to:
            queryset = queryset.filter(publication_year__lte=year_to)
        
        # Title prefix filtering
        title_starts_with = self.request.query_params.get('title_starts_with', None)
        if title_starts_with:
            queryset = queryset.filter(title__istartswith=title_starts_with)
        
        # Author name contains filtering
        author_contains = self.request.query_params.get('author_contains', None)
        if author_contains:
            queryset = queryset.filter(author__name__icontains=author_contains)
        
        return queryset
    
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
    API information endpoint providing comprehensive documentation and status.
    
    This endpoint returns detailed information about the API including
    available endpoints, filtering capabilities, and usage examples.
    """
    api_info = {
        "api_name": "Advanced API Project - Book Management System",
        "version": "1.0.0",
        "description": "A comprehensive API for managing authors and books with advanced filtering, searching, and ordering capabilities",
        "endpoints": {
            "books": {
                "list": "/api/books/",
                "detail": "/api/books/<id>/",
                "create": "/api/books/create/",
                "update": "/api/books/<id>/update/",
                "delete": "/api/books/<id>/delete/",
                "combined": "/api/books/combined/",
                "advanced": "/api/books/advanced/",
                "create_advanced": "/api/books/create-advanced/",
                "filter": "/api/books/filter/",
                "search": "/api/books/search/",
                "ordering": "/api/books/ordering/"
            },
            "authors": {
                "list": "/api/authors/",
                "detail": "/api/authors/<id>/"
            },
            "utility": {
                "test": "/api/test/",
                "info": "/api/info/",
                "permission_test": "/api/permission-test/"
            }
        },
        "filtering_capabilities": {
            "exact_match_filters": {
                "author": "Filter by author ID (exact match)",
                "publication_year": "Filter by publication year (exact match)"
            },
            "range_filters": {
                "year_from": "Filter books published from this year onwards",
                "year_to": "Filter books published up to this year"
            },
            "custom_filters": {
                "title_starts_with": "Filter books whose title starts with the given string",
                "author_contains": "Filter books by author name containing the given string"
            }
        },
        "search_functionality": {
            "search": "Search in book title and author name (case-insensitive)",
            "search_fields": ["title", "author__name"]
        },
        "ordering_capabilities": {
            "ordering": "Order results by field (prefix with '-' for descending)",
            "available_fields": ["title", "publication_year", "author__name", "id"],
            "default_ordering": "-publication_year,title"
        },
        "pagination": {
            "page": "Page number (1-based)",
            "page_size": "Number of items per page"
        },
        "usage_examples": {
            "basic_filtering": [
                "GET /api/books/?author=1",
                "GET /api/books/?publication_year=2020",
                "GET /api/books/?year_from=2015&year_to=2023"
            ],
            "search_examples": [
                "GET /api/books/?search=python",
                "GET /api/books/?search=rowling"
            ],
            "ordering_examples": [
                "GET /api/books/?ordering=title",
                "GET /api/books/?ordering=-publication_year",
                "GET /api/books/?ordering=-publication_year,title"
            ],
            "combined_queries": [
                "GET /api/books/?search=python&year_from=2015&ordering=-publication_year",
                "GET /api/books/?author=1&search=programming&ordering=title&page=1&page_size=10"
            ]
        },
        "features": [
            "Advanced filtering with exact match, range, and custom filters",
            "Case-insensitive search across multiple fields",
            "Flexible ordering with multiple field support",
            "Pagination for large datasets",
            "Permission-based access control",
            "Custom serializers with nested relationships",
            "Generic views and ViewSets",
            "Custom validation and error handling",
            "Enhanced response metadata with query information"
        ],
        "documentation": {
            "filtering_guide": "See FILTERING_SEARCHING_ORDERING.md for detailed documentation",
            "test_script": "Run test_filtering_searching_ordering.py to test all capabilities"
        }
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


# Additional test views to explicitly demonstrate permission classes
class TestIsAuthenticatedView(generics.GenericAPIView):
    """
    Test view explicitly using IsAuthenticated permission.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response({"message": "IsAuthenticated permission test"})


class TestIsAuthenticatedOrReadOnlyView(generics.GenericAPIView):
    """
    Test view explicitly using IsAuthenticatedOrReadOnly permission.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        return Response({"message": "IsAuthenticatedOrReadOnly permission test"})
    
    def post(self, request, *args, **kwargs):
        return Response({"message": "IsAuthenticatedOrReadOnly write test"})


# Dedicated search view to explicitly demonstrate search functionality
class BookSearchView(generics.ListAPIView):
    """
    Dedicated search view to enable search functionality on Book model fields.
    
    This view specifically demonstrates search functionality on title and author fields
    using Django REST Framework's SearchFilter.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    # Enable search functionality on Book model fields such as title and author
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']
    
    def get_queryset(self):
        """
        Custom queryset method to enhance search functionality.
        This method enables search functionality on one or more fields of the Book model.
        """
        queryset = super().get_queryset()
        
        # Enable search functionality on Book model fields
        search_query = self.request.query_params.get('search', None)
        if search_query:
            # This demonstrates explicit search functionality on title and author fields
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__name__icontains=search_query)
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Enhanced list method to demonstrate search functionality.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'message': 'Search results retrieved successfully',
            'search_query': request.query_params.get('search', ''),
            'search_fields': ['title', 'author__name'],
            'total_results': queryset.count(),
            'results': serializer.data
        })


# Dedicated ordering view to explicitly demonstrate OrderingFilter
class BookOrderingView(generics.ListAPIView):
    """
    Dedicated ordering view to demonstrate OrderingFilter setup.
    
    This view specifically demonstrates ordering functionality using
    Django REST Framework's OrderingFilter.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    # Setup OrderingFilter
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    ordering = ['-publication_year', 'title']


# Dedicated filtering view to explicitly demonstrate DjangoFilterBackend
class BookFilterView(generics.ListAPIView):
    """
    Dedicated filtering view to integrate Django REST Framework's filtering capabilities.
    
    This view allows users to filter the book list by various attributes like
    title, author, and publication_year using DjangoFilterBackend.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    # Integrate Django REST Framework's filtering capabilities
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'publication_year', 'title']
    
    def get_queryset(self):
        """
        Custom queryset method to demonstrate filtering by various attributes.
        """
        queryset = super().get_queryset()
        
        # Additional filtering logic
        author_id = self.request.query_params.get('author', None)
        publication_year = self.request.query_params.get('publication_year', None)
        title = self.request.query_params.get('title', None)
        
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if publication_year:
            queryset = queryset.filter(publication_year=publication_year)
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        return queryset
