class BankAccount:

    def __init__(self, account_number, holder):
        self.account_number = account_number
        self.holder = holder

    def __repr__(self):
        return f"Account number {self.account_number} Holder: {self.holder}"
