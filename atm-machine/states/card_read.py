from states.base import ATMState
from atm import ATM


class CardRead(ATMState):
    MAX_PIN_ATTEMPTS = 3

    def enter_pin(self, atm: ATM, pin: int):
        ## keep the session active
        atm.session.ping()

        ## check authentication
        if atm.bank.authenticate(atm.session.card, pin):
            atm.session.authenticated = True
            ## change the state
            from states.authenticated import AuthenticatedState

            atm.set_state(AuthenticatedState())
            atm.screen.show("You are authenticated. Proceed with a transaction!")
            return

        ## pin is wrong
        ## todo: count the number of wrong attempts

        atm.screen.show("You entered the wrong pin. Please start again!")

    def eject_card(self, atm: ATM):
        atm.card_reader.eject(atm.session.card)
        from states.idle_state import IdleState

        atm.set_state(IdleState())
        atm.session = None
        atm.screen.show("Card ejected. Thank you!")
