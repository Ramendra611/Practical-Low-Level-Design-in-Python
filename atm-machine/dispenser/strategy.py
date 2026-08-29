from abc import ABC, abstractmethod
from typing import Optional


class DispenseStrategy(ABC):

    @abstractmethod
    def plan(self, amount: int, inventory: dict[int, int]) -> Optional[dict[int, int]]:
        pass


class GreedyStrategy(DispenseStrategy):
    """
    Dispense by selecting the largest denomination first
    """

    def plan(self, amount, inventory):
        plan = {}
        remaining = amount

        for denomination in sorted(inventory.keys(), reverse=True):
            available = inventory[denomination]

            count = min(remaining // denomination, available)
            if count > 0:
                ## add this count in the plan
                plan[denomination] = count
                remaining = remaining - count * denomination
            if remaining == 0:  # the entire plan is done
                break

        return plan if remaining == 0 else None
