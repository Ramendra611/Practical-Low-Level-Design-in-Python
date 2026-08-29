from transaction.base import Transaction, TransactionResult
from models.account import BankAccount
from dispenser.dispenser import Dispenser
from bank.base import BankService


class WithdrawTransaction(Transaction):
    """
    Withdraw cash from an account

    1. Check the dispenser for the given amount
    2. Ask the bank to debit the amount ( bank will check the balance etc)
    3. Ask the Dispenser to give the cash
    4. Error Handling -> if the dispenser fails, then we have credit the amount back

    """

    def __init__(self, amount: int, account: BankAccount, dispenser: Dispenser):
        super().__init__(account)
        self.amount = amount
        self.dispenser = dispenser

    def execute(self, bank: BankService):
        # Step 1 : Check the dispenser for the given amount
        if not self.dispenser.can_dispense(self.amount):
            self.status = "Failed"  # todo: should come from some enum
            return TransactionResult.fail(
                message="Insufficient Cash in ATM", amount=self.amount
            )

        # Step 2 : Ask the bank to debit the amount
        if not bank.debit(account=self.account, amount=self.amount):
            self.status = "Failed"  # todo: should come from some enum
            return TransactionResult.fail(
                message="Insufficient funds in the account", amount=self.amount
            )

        # Step 3: Ask the Dispenser to give the cash
        try:
            self.dispenser.dispense(self.amount)
        except Exception as e:  # todo: Raise specific error DispenseError
            # undo the debit and credit the amount back to account
            bank.credit(account=self.account, amount=self.amount)
            self.status = "Failed"
            return TransactionResult.fail(
                message="Error while dispensing. Amount credited back to account",
                amount=self.amount,
            )

        self.status = "Success"  # todo: this should be from some enum
        return TransactionResult.success(
            message=f"Dispensed the { self.amount}",
            amount=self.amount,
        )
