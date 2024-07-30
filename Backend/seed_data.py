from applications.database import db
from applications.model import Section, Books
from datetime import datetime, timedelta
import random

def seed_books():
    # Clear existing data
    Books.query.delete()
    Section.query.delete()

    # Create sections
    sections = [
        Section(genre="Fiction"),
        Section(genre="Non-Fiction"),
        Section(genre="Science Fiction"),
        Section(genre="Mystery"),
        Section(genre="Biography")
    ]
    db.session.add_all(sections)
    db.session.commit()

    # List of sample books
    books = [
        {"name": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction"},
        {"name": "1984", "author": "George Orwell", "genre": "Fiction"},
        {"name": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction"},
        {"name": "A Brief History of Time", "author": "Stephen Hawking", "genre": "Non-Fiction"},
        {"name": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "genre": "Non-Fiction"},
        {"name": "Dune", "author": "Frank Herbert", "genre": "Science Fiction"},
        {"name": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "genre": "Science Fiction"},
        {"name": "The Da Vinci Code", "author": "Dan Brown", "genre": "Mystery"},
        {"name": "Gone Girl", "author": "Gillian Flynn", "genre": "Mystery"},
        {"name": "Steve Jobs", "author": "Walter Isaacson", "genre": "Biography"},
        {"name": "The Diary of a Young Girl", "author": "Anne Frank", "genre": "Biography"}
    ]

    # Add books to the database
    for book in books:
        section = Section.query.filter_by(genre=book["genre"]).first()
        new_book = Books(
            isbn_no=random.randint(1000000000, 9999999999),
            author=book["author"],
            price=random.randint(10, 50),
            name=book["name"],
            description=f"A {book['genre']} book by {book['author']}",
            date_published=datetime.now() - timedelta(days=random.randint(365, 3650)),
            section_id=section.id
        )
        db.session.add(new_book)

    db.session.commit()
    print("Database seeded successfully!")