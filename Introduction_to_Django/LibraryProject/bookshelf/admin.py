from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these columns
    search_fields = ('title', 'author')  # Add a search box for title and author
    list_filter = ('publication_year',)  # Add filter by publication year
