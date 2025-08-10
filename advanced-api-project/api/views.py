from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorListSerializer

# Create your views here.

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    View for listing all authors and creating new authors.
    
    Uses AuthorListSerializer for listing to avoid performance issues
    with nested book serialization.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting individual authors.
    
    Uses AuthorSerializer to provide full author details including
    nested book information.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    View for listing all books and creating new books.
    
    Includes author information and validates publication year.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting individual books.
    
    Provides full book details with author information.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer


@api_view(['GET'])
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
