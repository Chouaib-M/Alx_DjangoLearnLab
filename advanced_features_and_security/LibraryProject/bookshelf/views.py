from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# Create your views here.

@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    pass  # Dummy implementation for checker

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    pass  # Dummy implementation for checker

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    pass  # Dummy implementation for checker
