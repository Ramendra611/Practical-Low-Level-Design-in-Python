from abc import ABC, abstractmethod


class MembershipPolicy(ABC):

    @property
    @abstractmethod
    def max_books(self):
        pass

    @property
    @abstractmethod
    def loan_days(self):
        pass

    @property
    @abstractmethod
    def fine_per_day(self):
        pass

    def __repr__(self):
        return self.__class__.__name__
