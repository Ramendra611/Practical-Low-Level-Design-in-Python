from policies.base import MembershipPolicy


class GuestPolicy(MembershipPolicy):
    """Rules for guest members."""

    @property
    def max_books(self) -> int:
        return 1

    @property
    def loan_days(self) -> int:
        return 7

    @property
    def fine_per_day(self) -> float:
        return 10.0
