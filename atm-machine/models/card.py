class Card:
    def __init__(self, number, holder, expiry, account_number):
        self.number = number
        self.holder = holder
        self.expiry = expiry
        self.account_number = account_number

    def is_valid(self):
        """

        current date < expiry date
        :return: bool
        """
        return True  # todo : to check the expiry date

    def __repr__(self):
        return f"Card Number: {self.number} Holder:{self.holder}"
