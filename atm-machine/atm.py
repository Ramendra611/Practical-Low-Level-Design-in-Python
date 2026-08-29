from bank.base import BankService
from dispenser.dispenser import Dispenser
from hardware.hardware import CardReader, Keyboard, Screen, Printer
from states.idle_state import IdleState


class ATM:
    """
    Top level coordinator for everything


    """

    def __init__(
        self,
        bank,
        dispenser,
        card_reader=CardReader(),
        printer=Printer(),
        screen=Screen(),
        keyboard=Keyboard(),
    ):
        self.bank = bank
        self.screen = screen
        self.keyboard = keyboard
        self.dispenser = dispenser
        self.printer = printer
        self.card_reader = card_reader

        # -- state  of the atm ---
        self._state = IdleState()
        self.session = None
        self.screen.show("Welcome to the ATM! Please insert your card!")

    def set_state(self, state):
        self._state = state

    ## -- User Facing Actions --
    def insert_card(self, card):
        self._state.insert_card(self, card)

    def enter_pin(self, pin):
        self._state.enter_pin(self, pin)

    def select_transaction(self, txn):
        self._state.select_transaction(self, txn)

    def eject_card(self):
        self._state.eject_card(self)
