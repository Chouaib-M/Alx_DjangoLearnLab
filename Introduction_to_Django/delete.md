from bookshelf.models import Book

# Retrieve the book to delete
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"All books after deletion: {all_books}")
print(f"Number of books: {all_books.count()}")

