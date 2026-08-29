class CancellationPolicy:

    def __init__(
        self,
        fee_before_assignment: float = 0.0,
        fee_after_assignment: float = 10.0,
        fee_after_start: float = 50.0,
    ):
        self.free_before_assignment = fee_before_assignment
        self.fee_after_assignment = fee_after_assignment
        self.fee_after_start = fee_after_start

    def fee(self, trip) -> float:
        """
        Cancellation before assigned : 0 INR
        Cancellation after driver assigned : 10 INR
        Cancellation after started : 50 INR

        :param trip:
        :return:
        """

        if trip.started_at is not None:
            return self.fee_after_start

        if trip.driver is not None:
            return self.fee_after_assignment

        return self.free_before_assignment
