from datetime import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.book import Book
    from models.loan import Loan
    from models.member import Member


@dataclass(frozen=True)
class LibraryEvent:
    """
    The abstract base for all library events.
    """

    occurred_at: datetime


@dataclass(frozen=True)
class LoanIssuedEvent(LibraryEvent):
    """A member has successfully borrowed a copy."""

    loan: "Loan"


@dataclass(frozen=True)
class LoanReturnedEvent(LibraryEvent):
    loan: "Loan"
    fine_amount: float


@dataclass(frozen=True)
class ReservationFulfilledEvent(LibraryEvent):
    """
    A previously-reserved title now has an available copy for a
    specific member.
    """

    member: "Member"
    book: "Book"


class LoanOverdueEvent(LibraryEvent):

    loan: "Loan"
    days_overdue: int
