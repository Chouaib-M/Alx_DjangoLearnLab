from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer handles serialization of Book model instances.
    
    This serializer includes all fields of the Book model and implements
    custom validation to ensure publication_year is not in the future.
    It also provides a nested representation of the author relationship.
    """
    
    # Nested author representation (read-only to avoid circular references)
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_name']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication_year is not in the future.
        
        Args:
            value: The publication year value to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f'Publication year cannot be in the future. Current year is {current_year}.'
            )
        return value
    
    def validate(self, data):
        """
        Additional validation for the entire book data.
        
        This method can be used for cross-field validation if needed
        in the future.
        """
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer handles serialization of Author model instances.
    
    This serializer includes the author's name and dynamically serializes
    related books using the BookSerializer. The books field provides
    a nested representation of all books by the author.
    """
    
    # Nested books using BookSerializer
    books = BookSerializer(many=True, read_only=True)
    
    # Computed field for book count
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'book_count']
        read_only_fields = ['id', 'books', 'book_count']
    
    def get_book_count(self, obj):
        """
        Returns the total number of books by this author.
        
        Args:
            obj: The Author instance being serialized
            
        Returns:
            int: The number of books by the author
        """
        return obj.books.count()
    
    def to_representation(self, instance):
        """
        Custom representation method to handle nested serialization.
        
        This method ensures that the books are properly serialized
        and provides a clean, hierarchical representation of the data.
        """
        representation = super().to_representation(instance)
        return representation


class AuthorListSerializer(serializers.ModelSerializer):
    """
    Simplified AuthorSerializer for list views.
    
    This serializer excludes the nested books to avoid performance
    issues when listing multiple authors. It only includes basic
    author information and the book count.
    """
    
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count']
        read_only_fields = ['id', 'book_count']
    
    def get_book_count(self, obj):
        """Returns the total number of books by this author."""
        return obj.books.count() 