from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    LOST = "lost"


class BookCopy:
    def __init__(self, book, copy_id):
        self.book = book
        self.copy_id = copy_id
        self.status = BookStatus.AVAILABLE

    def __repr__(self) -> str:
        return (
            f"BookItem(copy_id={self.copy_id!r}, "
            f"title={self.book.title!r}, status={self.status.name})"
        )
