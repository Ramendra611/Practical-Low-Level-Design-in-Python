class RideSharingError(Exception):
    """Base class for all ride-sharing-system errors."""


class InvalidStateTransition(RideSharingError):
    """
    Raised when an operation is attempted from a state that does not
    permit it — for example, starting a trip that has already been
    completed, or cancelling a trip that was never requested.

    The state pattern enforces the transition graph; this exception
    is what a violation surfaces as to callers.
    """


class UnknownTripError(RideSharingError):
    """Raised when a caller references a trip ID the manager does not know."""


class UnknownDriverError(RideSharingError):
    """Raised when a caller references a driver ID the manager does not know."""


class DuplicateDriverError(RideSharingError):
    """Raised when register_driver is called with an already-registered ID."""


class NoDriverAvailableError(RideSharingError):
    """
    Raised when the matching strategy cannot find any eligible driver.

    Note: the matching strategy itself returns None rather than raising —
    that's the ordinary case, and callers frequently want to handle it
    without a try/except. This exception exists for callers who prefer
    exception-based flow, and can be raised by helper wrappers.
    """


class InsufficientBalanceError(RideSharingError):
    """Raised by WalletPayment when the wallet does not cover the fare."""
