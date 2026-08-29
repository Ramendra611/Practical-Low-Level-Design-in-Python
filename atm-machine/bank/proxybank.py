from models.account import BankAccount
from models.card import Card
from bank.base import BankService
from typing import Optional


class ProxyBank(BankService):
    """
    Store everything as dictionary
    """

    def __init__(self):
        self.accounts: dict[int, BankAccount] = {}  # todo: write this with type check
        self.balances: dict[int, float] = {}
        self.pins: dict[int, int] = {}

    def create_account(
        self, account: BankAccount, balance: int, card: Card, pin: int
    ) -> None:
        self.accounts[account.account_number] = account
        self.balances[account.account_number] = balance
        self.pins[card.number] = pin

    def get_account(self, account_number: str) -> Optional[BankAccount]:
        return self.accounts.get(account_number)

    def authenticate(self, card: Card, pin: int):
        return self.pins.get(card.number) == pin

    def debit(self, account: BankAccount, amount: float):
        # find the current balance
        balance = self.balances.get(account.account_number, 0)
        if balance < amount:
            return False
        # update the balance
        self.balances[account.account_number] = balance - amount
        return True

    def credit(self, account: BankAccount, amount: float):
        self.balances[account.account_number] = (
            self.balances.get(account.account_number, 0.0) + amount
        )
        return True
