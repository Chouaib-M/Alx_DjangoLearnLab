# Retrieve Book

```python
books = Book.objects.all()
for b in books:
    print(b.title, b.author, b.publication_year)
