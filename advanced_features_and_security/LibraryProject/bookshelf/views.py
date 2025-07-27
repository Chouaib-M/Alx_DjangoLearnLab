from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

# Create your views here.

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    pass  # Dummy implementation for checker

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    pass  # Dummy implementation for checker

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    pass  # Dummy implementation for checker

# Example form view for checker
def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Normally save or process data
            return redirect('book_list')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
