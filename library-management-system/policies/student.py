from policies.base import MembershipPolicy


class StudentPolicy(MembershipPolicy):
    """Rules for student members."""

    @property
    def max_books(self) -> int:
        return 3

    @property
    def loan_days(self) -> int:
        return 14

    @property
    def fine_per_day(self) -> float:
        return 5.0
