from abc import ABC, abstractmethod

from utils.exceptions import InsufficientBalanceError


class PaymentMethod(ABC):

    @abstractmethod
    def charge(self, final_fare, rider):
        pass


class UPIPayment(PaymentMethod):
    """UPI payment via VPA."""

    def __init__(self, upi_id: str):
        if "@" not in upi_id:
            raise ValueError("upi_id must be a valid VPA (contains '@')")
        self.upi_id = upi_id

    def charge(self, amount: float, from_user) -> None:
        # Stubbed — real integration talks to the UPI switch.
        return


class WalletPayment(PaymentMethod):
    """
    In-app wallet payment.

    Unlike the other methods, this one has real behaviour we can
    implement locally — it debits an internal balance. If the
    wallet cannot cover the amount, we raise
    InsufficientBalanceError; the caller (RideManager) can decide
    whether to fall back to another payment method, prompt the
    rider to top up, or record the trip as unpaid.
    """

    def __init__(self, balance: float):
        if balance < 0:
            raise ValueError("Wallet balance cannot be negative")
        self.balance = balance

    def charge(self, amount: float, from_user) -> None:
        if amount > self.balance:
            raise InsufficientBalanceError(
                f"Wallet has {self.balance:.2f}, fare is {amount:.2f}"
            )
        self.balance -= amount



class CardPayment(PaymentMethod):
    """
    Credit or debit card payment via an external gateway.

    We hold only the last-four for display and receipts; the full
    card number and CVV would live in a PCI-compliant vault, not
    in this object.
    """

    def __init__(self, card_last4: str):
        if len(card_last4) != 4 or not card_last4.isdigit():
            raise ValueError("card_last4 must be four digits")
        self.card_last4 = card_last4

    def charge(self, amount: float, from_user) -> None:
        # In production: call the card gateway, handle timeouts and
        # decline codes, persist the transaction ID. Stubbed here.
        return


class CashPayment(PaymentMethod):
    """
    Cash paid directly to the driver.

    The system merely records that cash was the settlement method;
    there's nothing to charge programmatically.
    """

    def charge(self, amount: float, from_user) -> None:
        # Cash is settled in person. Nothing to do here.
        return


class PaymentFactory:

    @staticmethod
    def create(kind, **kwargs):
        kind = kind.lower()
        if kind == "cash":
            return CashPayment()
        if kind == "card":
            return CardPayment(card_last4=kwargs["card_last4"])
        if kind == "upi":
            return UPIPayment(upi_id=kwargs["upi_id"])
        if kind == "wallet":
            return WalletPayment(balance=kwargs["balance"])
        raise ValueError(f"Unknown payment kind: {kind!r}")