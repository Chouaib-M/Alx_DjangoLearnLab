from django.contrib import admin
from .models import Author, Book

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.
    
    Provides a clean interface for managing authors with search
    and filtering capabilities.
    """
    list_display = ['name', 'get_book_count']
    search_fields = ['name']
    ordering = ['name']
    
    def get_book_count(self, obj):
        """Display the number of books by this author."""
        return obj.get_book_count()
    get_book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.
    
    Provides comprehensive book management with author filtering,
    search capabilities, and publication year validation.
    """
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_year', 'title']
    autocomplete_fields = ['author']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related for author."""
        return super().get_queryset(request).select_related('author')
