from relationship_app.models import Author, Book, Library, Librarian

def query_samples():
    # Query all books by a specific author
    author = Author.objects.first()  # get first author
    if author:
        books_by_author = Book.objects.filter(author=author)
        print(f"Books by {author.name}:")
        for book in books_by_author:
            print(book.title)

    # List all books in a library
    library = Library.objects.first()
    if library:
        print(f"\nBooks in library '{library.name}':")
        for book in library.books.all():
            print(book.title)

    # Retrieve the librarian for a library
    if library:
        librarian = Librarian.objects.filter(library=library).first()
        if librarian:
            print(f"\nLibrarian for '{library.name}': {librarian.name}")
        else:
            print(f"\nNo librarian found for '{library.name}'")

if __name__ == "__main__":
    query_samples() 