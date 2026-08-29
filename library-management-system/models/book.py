from models.book_copy import BookCopy, BookStatus
from typing import Optional


class Book:

    def __init__(self, title, isbn, author, category):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.category = category
        ## how to have book v/s book item

        self.copies: list[BookCopy] = []

    def add_copy(self, copy: BookCopy):
        self.copies.append(copy)

    def available_copy(self) -> Optional[BookCopy]:
        """
        return an avaiable copy for the book
        :return:
        """
        # available_copy = [copy  for copy in self.copies if copy.status == BookStatus.Available]
        # return available_copy if available_copy else None # todo: check this logic

        return next(
            (c for c in self.copies if c.status == BookStatus.AVAILABLE),
            None,
        )

    def total_copies(self):
        return len(self.copies)


if __name__ == "__main__":

    design_patterns = Book(
        "Design Patterns", "1234", author="Eric Freeman", category="CS"
    )

    design_patterns_copy1 = BookItem
