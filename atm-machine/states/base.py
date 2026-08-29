from abc import ABC, abstractmethod
from utils.exceptions import InvalidOperation

# from atm import ATM


class ATMState(ABC):

    def insert_card(self, atm: "ATM", card):
        raise InvalidOperation(f"Cannot insert card in state: {self.name()} ! ")

    def enter_pin(self, atm: "ATM", pin: int):
        raise InvalidOperation(f"Cannot enter pin in state: {self.name()} ! ")

    def select_transaction(self, txn, atm: "ATM"):
        raise InvalidOperation(f"Cannot select transaction in state: {self.name()} ! ")

    def eject_card(self, atm: "ATM"):
        raise InvalidOperation(f"Cannot eject card in state: {self.name()} ! ")

    def name(self):
        return self.__class__.__name__  # todo: we can check later
