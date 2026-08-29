from states.base import ATMState


class TransactionActiveState(ATMState):

    def __init__(self, transaction):
        self.transaction = transaction

    def execute(self, atm):
        try:
            result = self.transaction.execute(atm.bank)
        except Exception as e:
            atm.screen.show("Something went wrong in the transaction!")
            ## todo: go back to authentication
            self._return_to_authenticated_state(atm)
            return

        ## if success then print the receipt
        if self.transaction.status == "SUCCESS":
            self.print_reciept(atm, result)

        self._return_to_authenticated_state(atm)

    def _return_to_authenticated_state(self, atm):
        from states.authenticated import AuthenticatedState

        atm.set_state(AuthenticatedState())
        atm.screen.show("Pls continue with another transaction or eject the card!")

    def print_reciept(self, atm, result):
        pass  # todo: print the reciept later
