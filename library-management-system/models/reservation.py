from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime

if TYPE_CHECKING:
    from models.book import Book
    from models.member import Member


@dataclass
class Reservation:

    member: "Member"
    book: "Book"
    reserved_at: datetime = field(default_factory=datetime.now)

    def __repr__(self) -> str:
        return (
            f"Reservation(member={self.member.name!r}, "
            f"title={self.book.title!r}, "
            f"at={self.reserved_at.isoformat(timespec='seconds')})"
        )
