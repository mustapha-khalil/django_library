def convertQuerySetToList(books):
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "publication_year": book.publication_year,
            "category": book.category,
        }
        for book in books
    ]
