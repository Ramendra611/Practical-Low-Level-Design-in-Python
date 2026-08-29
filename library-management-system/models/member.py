from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.loan import Loan
    from policies.base import MembershipPolicy


class Member:
    def __init__(self, member_id, name, email, policy):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.policy = policy

        self.active_loans: list["Loan"] = []

    def can_borrow_more(self):
        return len(self.active_loans) < self.policy.max_books
