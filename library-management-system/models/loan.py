import uuid
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional


class Loan:

    def __init__(self, member, book_copy):
        self.id = str(uuid.uuid4())[:8]
        self.member = member
        self.book_item = book_copy
        self.issue_date: datetime = datetime.now()
        self.due_date: datetime = self.issue_date + timedelta(
            days=member.policy.loan_days
        )
        self.return_date: Optional[datetime] = None

    @property
    def is_overdue(self) -> bool:
        """
        True if the loan is past its due date AND still open. A
        returned loan is not overdue; it is done.
        """
        return not self.is_returned and datetime.now() > self.due_date

    @property
    def is_returned(self) -> bool:
        """True once the loan has been closed."""
        return self.return_date is not None

    def calculate_fine(self, as_of: Optional[datetime] = None) -> float:
        end_date = self.return_date or as_of or datetime.now()
        if end_date <= self.due_date:
            return 0.0

        overdue_days = (end_date - self.due_date).days + 1
        return overdue_days * self.member.policy.fine_per_day

    def __repr__(self) -> str:
        status = "returned" if self.is_returned else "active"
        return (
            f"Loan(id={self.id!r}, "
            f"member={self.member.name!r}, "
            f"title={self.book_item.book.title!r}, "
            f"due={self.due_date.date().isoformat()}, "
            f"status={status})"
        )
