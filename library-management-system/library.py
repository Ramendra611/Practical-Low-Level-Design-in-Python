from collections import deque
from datetime import datetime
from typing import Optional

from utils.exceptions import (
    BorrowingLimitExceeded,
    DuplicateMemberError,
    NoAvailableCopyError,
    UnknownBookError,
    UnknownLoanError,
    UnknownMemberError,
)

from models.book import Book
from models.book_copy import BookStatus
from models.loan import Loan
from models.member import Member
from models.reservation import Reservation
from notifications.events import (
    LibraryEvent,
    LoanIssuedEvent,
    LoanReturnedEvent,
    ReservationFulfilledEvent,
)

from notifications.listener import LibraryEventListener
from search.book_search import BookSearch


class Library:
    """
    Main functionalities
        add_book
        add_member
        add_listener
        search

        borrow
        return book
        reserve
    """

    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        self.active_loans: dict[str, Loan] = {}
        # Reservation queues, keyed by ISBN.
        self.reservations: dict[str, deque[Reservation]] = {}

        self._listeners: list[LibraryEventListener] = []

    def add_member(self, member: Member) -> None:
        """
        Register a new member. Duplicate member IDs are a hard error
        rather than a silent ignore, because they usually indicate a
        real registration bug the caller wants to know about.
        """
        if member.member_id in self.members:
            raise DuplicateMemberError(f"Member {member.member_id!r} already exists.")
        self.members[member.member_id] = member

    def add_listener(self, listener: LibraryEventListener) -> None:
        """
        Subscribe a listener to library events. Called during
        composition — typically in `main.py` — after the library is
        constructed and before any operations run.
        """
        self._listeners.append(listener)

    def add_book(self, book: Book) -> None:
        """
        Add a book to the catalog.

        Idempotent on ISBN — re-adding a book with the same ISBN is
        silently ignored rather than overwriting. This matches the
        real-world case where a librarian re-processes a shipment and
        we don't want to blow away the existing copy list.
        """
        if book.isbn in self.books:
            return
        self.books[book.isbn] = book

    @property
    def search(self) -> BookSearch:
        """

        Returning a search interface which will further return the list of books
        :return:
        """
        return BookSearch(list(self.books.values()))

    def borrow(self, member_id: str, isbn: str):
        """

        1. Member should be valid
        2. book should exist
        3. member should be eligible to take the book
        4. book should be available

        success: create a loan object
        fail: raise some error ( LibraryError)

        :return:
        """

        member = self._require_member(member_id)
        book = self._require_book(isbn)

        ## if member is not eligible then raise error
        if not member.can_borrow_more():
            raise BorrowingLimitExceeded(
                f"{member.name} is at the {member.policy} limit of "
                f"{member.policy.max_books} concurrent loans."
            )

        ## book is available or not
        copy = book.available_copy()
        if copy is None:
            ## todo: we can create a default reservation for that book
            raise NoAvailableCopyError(f"No copies of {book.title!r} are available.")

        copy.status = BookStatus.BORROWED
        loan = Loan(member, copy)
        member.active_loans.append(loan)  # the loan is attached to the member
        self.active_loans[loan.id] = (
            loan  # the loan is attached to the list of loans of the library
        )

        self._emit(LoanIssuedEvent(occurred_at=datetime.now(), loan=loan))
        return loan

    def return_book(self, loan_id: str) -> float:
        """

        close a loan

        Steps:
        1. Check the loan
        2. create the return timestamp
        3. look at fine if applicable
        4. change the stats of the book to "AVAILABLE"
        5. remove the loan from the member and from the library
        6. create LoanReturnedEvent
        7. check if there is any reservation (queue) for that book, if yes, fulfil the reservation
            trigger the event ReservationFulfilledEvent


        :param loan_id:
        :return:
        """

        loan = self._require_loan(loan_id)

        loan.return_date = datetime.now()

        fine = loan.calculate_fine()

        # Free the copy for the next borrower.
        loan.book_item.status = BookStatus.AVAILABLE

        # Remove from active tracking. Both structures must be updated
        # or the two views of "active loans" fall out of sync.
        del self.active_loans[loan_id]
        loan.member.active_loans.remove(loan)

        self._emit(
            LoanReturnedEvent(occurred_at=datetime.now(), loan=loan, fine_amount=fine)
        )

        # If someone is waiting on this title, they get the notification.
        self._fulfill_next_reservation(loan.book_item.book)

        return fine

    def reserve(self, member_id: str, isbn: str) -> Optional[Reservation]:
        """
        Add a reservation for this member on this title.

        1. check if member is valid
        2. check if book is valid
        """
        member = self._require_member(member_id)
        book = self._require_book(isbn)

        if book.available_copy() is not None:
            # A copy is right there. Do not queue; tell the caller.
            return None
        # if the book is not available
        reservation = Reservation(member=member, book=book)
        self.reservations.setdefault(isbn, deque()).append(reservation)
        return reservation

    ## Some internal helper methods

    def _fulfill_next_reservation(self, book: Book):
        """
         Check if there is reservation queue for this book

        :param book:
        :return:
        """

        reservation_queue = self.reservations.get(book.isbn)
        if not reservation_queue:
            return

        next_reservation = reservation_queue.popleft()
        self._emit(
            ReservationFulfilledEvent(
                occurred_at=datetime.now(),
                member=next_reservation.member,
                book=book,
            )
        )

    def _emit(self, event: LibraryEvent):
        """
        Dispach and event to all the listeners

        :param event:
        :return:
        """
        for listener in self._listeners:
            listener.on_event(event)

    def _require_member(self, member_id: str) -> Member:
        """Fetch a member by ID or raise UnknownMemberError."""
        try:
            return self.members[member_id]
        except KeyError:
            raise UnknownMemberError(f"No such member: {member_id!r}") from None

    def _require_book(self, isbn: str) -> Book:
        """Fetch a book by ISBN or raise UnknownBookError."""
        try:
            return self.books[isbn]
        except KeyError:
            raise UnknownBookError(f"No such book (ISBN {isbn!r}).") from None

    def _require_loan(self, loan_id: str) -> Loan:
        """Fetch an active loan by ID or raise UnknownLoanError."""
        try:
            return self.active_loans[loan_id]
        except KeyError:
            raise UnknownLoanError(f"No such active loan: {loan_id!r}") from None
