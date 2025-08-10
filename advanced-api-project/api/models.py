from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# Create your models here.

class Author(models.Model):
    """
    Author model represents a book author.
    
    This model stores basic information about authors and establishes
    a one-to-many relationship with books through the Book model's
    foreign key reference.
    """
    name = models.CharField(
        max_length=200,
        help_text="The full name of the author"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"
    
    def __str__(self):
        return self.name
    
    def get_book_count(self):
        """Returns the total number of books by this author."""
        return self.book_set.count()


class Book(models.Model):
    """
    Book model represents a published book.
    
    This model stores book information and maintains a foreign key
    relationship with the Author model, allowing multiple books
    to be associated with a single author.
    """
    title = models.CharField(
        max_length=300,
        help_text="The title of the book"
    )
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000, message="Publication year must be at least 1000"),
            MaxValueValidator(datetime.now().year, message="Publication year cannot be in the future")
        ],
        help_text="The year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author of this book"
    )
    
    class Meta:
        ordering = ['-publication_year', 'title']
        verbose_name = "Book"
        verbose_name_plural = "Books"
        # Ensure unique combination of title and author
        unique_together = ['title', 'author']
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    def clean(self):
        """Custom validation to ensure publication year is not in the future."""
        from django.core.exceptions import ValidationError
        current_year = datetime.now().year
        if self.publication_year > current_year:
            raise ValidationError({
                'publication_year': f'Publication year cannot be in the future. Current year is {current_year}.'
            })
