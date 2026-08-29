from dispenser.strategy import DispenseStrategy


class Dispenser:
    """
    Manage the cash inventor and coordinate the dispensing

    """

    def __init__(
        self, inventory: dict[int, int], strategy: DispenseStrategy
    ):  # todo: add hint for strategy
        self.inventory = inventory
        self.strategy = strategy

    def can_dispense(self, amount):
        return self.strategy.plan(amount, self.inventory) is not None

    def dispense(self, amount: float):
        """
        plan based on the strategy --> return the denominations
        dispense the amount based on the denominations
        """
        plan = self.strategy.plan(amount, self.inventory)
        if plan is None:
            # raise some error
            raise Exception("Cannot dispense the amount!!")  # todo: custom error

        for denomination, count in plan.items():
            # reduce that amount from the inventory
            self.inventory[denomination] -= count
        return plan

    def restock(self, denomination: int, count: int):
        self.inventory[denomination] = self.inventory.get(denomination, 0) + count

    def inventory_summary(self):
        pass
