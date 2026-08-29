# create a bank
from bank.proxybank import ProxyBank
from dispenser.dispenser import Dispenser
from dispenser.strategy import GreedyStrategy
from models.account import BankAccount
from models.card import Card
from atm import ATM
from transaction.withdraw import WithdrawTransaction
import traceback


def create_bank():
    ramesh_account = BankAccount(account_number=34343434, holder="Ramesh")
    ramesh_card = Card(
        number="123-456-789",
        holder="Ramesh",
        expiry="2026-09-09",
        account_number=34343434,
    )
    bank = ProxyBank()

    bank.create_account(ramesh_account, balance=10000, card=ramesh_card, pin=1234)
    return bank, ramesh_account, ramesh_card


# crete an atm
def create_atm(bank):
    dispenser = Dispenser(
        {
            2000: 5,
            500: 10,
            200: 5,
            100: 8,
        },
        strategy=GreedyStrategy(),
    )
    return ATM(bank=bank, dispenser=dispenser)


# do a logical flow of the code

try:
    bank, ramesh_account, ramesh_card = create_bank()
except Exception as e:
    print("Error in creating bank ", e)
    traceback.print_exc()

try:
    atm = create_atm(bank)
except Exception as e:
    print("Error in creating atm ", e)
    traceback.print_exc()

print("bank and atm created successfully!!!")

try:
    atm.insert_card(ramesh_card)
    atm.enter_pin(pin=1234)
    atm.select_transaction(
        WithdrawTransaction(
            account=ramesh_account, amount=500, dispenser= atm.dispenser
        )
    )

except Exception as e:
    traceback.print_exc()
