from models.book import Book
from typing import Optional


class BookSearch:

    def __init__(self, books: list[Book]):
        self._books = books

    def by_title(self, query: str) -> list[Book]:
        """
        searching by direct string comparison
        OUT OF SCOPE: fuzzy searching algorithms
        """
        q = query.lower()
        return [b for b in self._books if q in b.title.lower()]

    def by_isbn(self, query: str) -> Optional[Book]:
        return next((b for b in self._books if b.isbn == query), None)
        """
        result = [b for b in self._books if b.isbn == isbn]
        return result[0] if result else None

        """

    def by_author(self, query: str) -> list[Book]:
        q = query.lower()
        return [b for b in self._books if q in b.author.lower()]

    def by_category(self, query: str) -> list[Book]:
        return [b for b in self._books if b.category.lower() == query.lower()]
