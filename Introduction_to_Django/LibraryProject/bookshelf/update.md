from bookshelf.models import Book

# Retrieve the book to update
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm the update
print(f"Updated book title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
