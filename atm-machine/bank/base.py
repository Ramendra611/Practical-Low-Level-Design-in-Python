from abc import ABC, abstractmethod
from models.card import Card


class BankService(ABC):
    @abstractmethod
    def authenticate(self, card: Card, pin: str):
        pass

    @abstractmethod
    def get_account(self, account):
        pass

    # @abstractmethod
    # def check_balance(self, account):
    #     pass

    @abstractmethod
    def debit(self, account, amount):
        pass

    @abstractmethod
    def credit(self, account, amount):
        pass

    def transfer(self, source, destination, amount):
        pass
