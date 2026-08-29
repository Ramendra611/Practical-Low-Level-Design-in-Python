"""
Domain-specific exceptions for the library system.

Why a dedicated exceptions module?

The library has several failure modes — an unknown member ID, an
unknown book, a member already at their borrowing limit, no available
copy — that callers may want to handle differently. Raising a bare
`ValueError` or `KeyError` for all of them forces the caller to
inspect exception messages to distinguish cases, which is brittle.

Distinct exception classes let callers write clean handlers:

    try:
        loan = library.borrow(member_id, isbn)
    except BorrowingLimitExceeded:
        show_upgrade_membership_prompt()
    except NoAvailableCopyError:
        offer_reservation()
    except UnknownMemberError:
        redirect_to_registration()

All library exceptions inherit from a single `LibraryError` base so
callers who want to catch "anything from the library" can do so with
one `except` clause.
"""


class LibraryError(Exception):
    """
    Base class for all library-specific exceptions.

    A caller who wants to catch any library problem — without caring
    about the specific kind — can catch this one class.
    """


class UnknownMemberError(LibraryError):
    """Raised when a member_id is not registered in the library."""


class UnknownBookError(LibraryError):
    """Raised when an ISBN is not in the catalog."""


class UnknownLoanError(LibraryError):
    """Raised when a loan_id is not among the active loans."""


class DuplicateMemberError(LibraryError):
    """Raised on attempt to register a member with an existing member_id."""


class BorrowingLimitExceeded(LibraryError):
    """
    Raised when a member tries to borrow but is already at the maximum
    number of concurrent loans their policy allows.
    """


class NoAvailableCopyError(LibraryError):
    """
    Raised when a borrow is requested for a title whose copies are
    all currently on loan or lost. Callers typically respond by
    offering a reservation.
    """
