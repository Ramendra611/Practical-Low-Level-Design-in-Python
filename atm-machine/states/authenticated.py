from states.base import ATMState
from atm import ATM


class AuthenticatedState(ATMState):
    def select_transaction(self, atm: ATM, transaction):
        # check if session is valid

        if atm.session.is_timed_out():
            self._handle_timeout(atm)
            return

        atm.session.ping()
        from states.transaction_active import TransactionActiveState

        new_state = TransactionActiveState(transaction)
        atm.set_state(new_state)
        atm.screen.show(
            "Processing the transaction"
        )  # todo: display the name of transaction
        new_state.execute(atm)

    def eject_card(self, atm: ATM):
        atm.card_reader.eject(atm.session.card)
        from states.idle_state import IdleState

        atm.set_state(IdleState())
        atm.session = None
        atm.screen.show("Card is ejected! Thank you!")

    def _handle_timeout(self, atm):
        atm.card_reader.eject(atm.session.card)
        from states.idle_state import IdleState

        atm.set_state(IdleState())
        atm.session = None
        atm.screen.show("Session timed out. Card returned.")

    ## todo: handle the timeout
