from states.base import ATMState

# from atm import ATM
from models.session import Session


class IdleState(ATMState):
    def insert_card(self, atm: "ATM", card):
        ## check if the card is valid
        if not card.is_valid():  # if the card is invalid
            ## show the message on screen
            atm.screen.show("Card is expired!!")
            ## eject the card
            atm.card_reader.eject(card)
            return

        ## start  a session
        atm.session = Session(card=card)

        ## change the state --> CardRead
        from states.card_read import CardRead  # todo: check the circular import issie

        atm.set_state(CardRead())
        atm.screen.show("Enter the pin: ")
