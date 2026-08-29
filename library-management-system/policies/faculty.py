from policies.base import MembershipPolicy


class FacultyPolicy(MembershipPolicy):
    """Rules for faculty members."""

    @property
    def max_books(self) -> int:
        return 10

    @property
    def loan_days(self) -> int:
        return 30

    @property
    def fine_per_day(self) -> float:
        return 2.0
