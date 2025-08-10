from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorListSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, BookActionPermission


class BookViewSet(viewsets.ModelViewSet):
    """
    Advanced ViewSet for Book model using Django REST Framework's ViewSet.
    
    This ViewSet provides all CRUD operations in a single class with
    custom actions and advanced filtering capabilities.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [BookActionPermission]
    
    # Advanced filtering and searching
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['-publication_year', 'title']
    
    def get_queryset(self):
        """
        Custom queryset method to add dynamic filtering.
        
        This method allows for complex filtering based on query parameters
        and demonstrates advanced queryset manipulation.
        """
        queryset = Book.objects.select_related('author').all()
        
        # Filter by publication year range
        min_year = self.request.query_params.get('min_year', None)
        max_year = self.request.query_params.get('max_year', None)
        
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)
        if max_year:
            queryset = queryset.filter(publication_year__lte=max_year)
        
        # Filter by author name (case-insensitive)
        author_name = self.request.query_params.get('author_name', None)
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
        
        # Filter by book title (case-insensitive)
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def recent_books(self, request):
        """
        Custom action to get recently published books.
        
        This action demonstrates how to add custom endpoints to a ViewSet
        and provides a filtered list of recent books.
        """
        recent_books = self.get_queryset().order_by('-publication_year')[:5]
        serializer = self.get_serializer(recent_books, many=True)
        
        return Response({
            'message': 'Recent books retrieved successfully',
            'count': len(recent_books),
            'books': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def book_statistics(self, request):
        """
        Custom action to get book statistics.
        
        This action provides aggregated data about books and demonstrates
        how to perform database aggregations in custom actions.
        """
        total_books = Book.objects.count()
        total_authors = Author.objects.count()
        books_by_year = Book.objects.values('publication_year').annotate(
            count=Count('id')
        ).order_by('-publication_year')[:10]
        
        return Response({
            'total_books': total_books,
            'total_authors': total_authors,
            'books_by_year': list(books_by_year),
            'message': 'Book statistics retrieved successfully'
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def duplicate_book(self, request, pk=None):
        """
        Custom action to duplicate an existing book.
        
        This action demonstrates how to perform custom operations on
        individual objects and handle complex business logic.
        """
        book = self.get_object()
        
        # Create a duplicate book with modified title
        duplicate_title = f"{book.title} (Copy)"
        duplicate_book = Book.objects.create(
            title=duplicate_title,
            author=book.author,
            publication_year=book.publication_year
        )
        
        serializer = self.get_serializer(duplicate_book)
        
        return Response({
            'message': f'Book "{book.title}" duplicated successfully',
            'original_book': {
                'id': book.id,
                'title': book.title,
                'author': book.author.name
            },
            'duplicate_book': serializer.data
        }, status=status.HTTP_201_CREATED)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Advanced ViewSet for Author model with custom actions.
    
    This ViewSet demonstrates ViewSet usage for authors with
    custom actions and advanced filtering.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """
        Dynamic serializer selection based on action.
        
        This method demonstrates how to use different serializers
        for different actions to optimize performance.
        """
        if self.action == 'list':
            return AuthorListSerializer
        return AuthorSerializer
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def books_by_author(self, request, pk=None):
        """
        Custom action to get all books by a specific author.
        
        This action provides a focused view of an author's works
        and demonstrates detail-level custom actions.
        """
        author = self.get_object()
        books = author.books.all()
        serializer = BookSerializer(books, many=True)
        
        return Response({
            'author': {
                'id': author.id,
                'name': author.name
            },
            'books_count': len(books),
            'books': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def prolific_authors(self, request):
        """
        Custom action to get authors with the most books.
        
        This action demonstrates advanced database queries and
        aggregation to find prolific authors.
        """
        prolific_authors = Author.objects.annotate(
            book_count=Count('books')
        ).filter(book_count__gt=0).order_by('-book_count')[:5]
        
        serializer = AuthorListSerializer(prolific_authors, many=True)
        
        return Response({
            'message': 'Prolific authors retrieved successfully',
            'authors': serializer.data
        })


class BookAdvancedListView(generics.ListAPIView):
    """
    Advanced ListView with custom filtering and pagination.
    
    This view demonstrates advanced list functionality with
    custom filtering, searching, and response formatting.
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """
        Advanced queryset with complex filtering logic.
        
        This method demonstrates how to implement sophisticated
        filtering and searching capabilities.
        """
        queryset = Book.objects.select_related('author').all()
        
        # Advanced search functionality
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(publication_year__icontains=search_query)
            )
        
        # Advanced filtering
        author_id = self.request.query_params.get('author_id', None)
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        year_from = self.request.query_params.get('year_from', None)
        year_to = self.request.query_params.get('year_to', None)
        
        if year_from:
            queryset = queryset.filter(publication_year__gte=year_from)
        if year_to:
            queryset = queryset.filter(publication_year__lte=year_to)
        
        # Custom ordering
        order_by = self.request.query_params.get('order_by', '-publication_year')
        if order_by in ['title', '-title', 'publication_year', '-publication_year', 'author__name', '-author__name']:
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('-publication_year', 'title')
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Custom list method with enhanced response formatting.
        
        This method demonstrates how to customize the response
        format and add additional metadata.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Add pagination if needed
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['total_count'] = queryset.count()
            response.data['filtered_count'] = len(page)
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'message': 'Books retrieved successfully',
            'total_count': queryset.count(),
            'books': serializer.data,
            'filters_applied': {
                'search': self.request.query_params.get('search'),
                'author_id': self.request.query_params.get('author_id'),
                'year_from': self.request.query_params.get('year_from'),
                'year_to': self.request.query_params.get('year_to'),
                'order_by': self.request.query_params.get('order_by', '-publication_year')
            }
        })


class BookCreateWithValidationView(generics.CreateAPIView):
    """
    Advanced CreateView with custom validation and business logic.
    
    This view demonstrates how to implement complex creation logic
    with custom validation and error handling.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom creation logic with validation and business rules.
        
        This method demonstrates how to implement complex business
        logic during object creation.
        """
        # Get the author to check if they exist
        author_id = serializer.validated_data.get('author').id
        author = get_object_or_404(Author, id=author_id)
        
        # Check if the book already exists for this author
        title = serializer.validated_data.get('title')
        existing_book = Book.objects.filter(
            title=title,
            author=author
        ).first()
        
        if existing_book:
            from rest_framework import serializers
            raise serializers.ValidationError({
                'title': f'A book with title "{title}" already exists for author {author.name}.'
            })
        
        # Create the book
        book = serializer.save()
        
        # Log the creation (in a real application, you'd use proper logging)
        print(f"New book created: {book.title} by {book.author.name} in {book.publication_year}")
        
        return book
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method with enhanced error handling.
        
        This method demonstrates how to provide better error messages
        and response formatting during creation.
        """
        try:
            response = super().create(request, *args, **kwargs)
            response.data['message'] = 'Book created successfully'
            response.data['status'] = 'success'
            return response
        except Exception as e:
            return Response({
                'message': 'Failed to create book',
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST) 