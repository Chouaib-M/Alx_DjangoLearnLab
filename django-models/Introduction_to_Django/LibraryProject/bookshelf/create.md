from bookshelf.models import Book

# Create and save in one step
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Book created: {book.title} by {book.author} ({book.publication_year})")
