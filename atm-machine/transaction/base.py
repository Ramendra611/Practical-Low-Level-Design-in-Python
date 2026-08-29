from abc import ABC, abstractmethod
from typing import Any

from bank.base import BankService


class TransactionResult:
    """
    Either Success or Fail
    """

    def __init__(self, success: bool, message: str = "", amount: Any = None):
        self.success = success
        self.message = message
        self.amount = amount

    @classmethod
    def success(cls, amount, message):
        return cls(success=True, amount=amount, message=message)

    @classmethod
    def fail(cls, amount, message):
        return cls(
            success=False, amount=amount, message=message
        )  # alternate constructor


class TransactionStatus:
    """
    Pending,

    """

    pass


class Transaction(ABC):

    def __init__(self, account):
        self.account = account
        self.status = "Pending"  # todo: this should be enum

    def execute(
        self, bank: BankService
    ) -> TransactionResult:  # todo: what it should return
        pass
