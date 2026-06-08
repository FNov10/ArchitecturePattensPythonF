from dataclasses import dataclass
from collections import namedtuple
from typing import NamedTuple
import  pytest
@dataclass(frozen=True)
class Name:
    first_name: str
    last_name: str

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Money(NamedTuple):
    currency: str
    value: int

    def __add__(self, money2: "Money"):
        if self._can_add(money2):
            return Money(self.currency, self.value + money2.value)
        else:
            raise ValueError("Cannot add two different currencies!")

    def __sub__(self, money2: "Money"):
        if self._can_subtract(money2):
            return Money(self.currency, self.value - money2.value)
        else: raise ValueError("Cannot subtract two different currencies!")


    def _can_add(self, money: "Money"):
        return self.currency==money.currency

    def _can_subtract(self, money: "Money"):
        return all(
            [self.currency==money.currency, self.value>money.value]
        )

    def __str__(self):
        return f"{self.currency} {self.value}"

Line = namedtuple('Line', ['sku', 'qty'])
x = Money("AED", 40)
def test_equality():
    assert Money("GBP", 40) == Money("GBP", 40)
    x = Name("Fahad", "Naveed")
    y = Name("Fahad","Naveed")
    assert(x!=y)

fiver = Money("AED", 5)
tenner = Money("AED", 10)
def test_can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner

def test_can_subtract_money_values():
    assert tenner - fiver == fiver

def test_adding_different_currencies_fails():
    with pytest.raises(ValueError):
        Money('usd', 10) + Money('CAD', 20)



