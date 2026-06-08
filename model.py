from dataclasses import dataclass
from datetime import date
from typing import Optional, List
from sqlalchemy import false


@dataclass(frozen=True)
class OrderLine:
    # This is a value object
    orderid: str #Order reference. Different orderlines can have the same orderid
    qty: int
    sku: str

class Batch:
    def __init__(
            self,
            ref: str,
            sku: str,
            qty: int,
            eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_qty = qty
        self._allocated_lines = set()

    def __lt__(self, other):
        if self.eta==None:
            return True
        if other.eta==None:
            return False
        return self.eta<other.eta

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return false
        return self.reference == other.reference

    def __str__(self):
        return (f"Batch {self.sku} with ref {self.reference}, available quantity of"
                f" {self.available_quantity}, and an ETA of {self.eta}")

    def __hash(self):
        return hash(self.reference)

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocated_lines.add(line)

    def deallocate(self, line: OrderLine):
        if self.can_deallocate(line):
            self._allocated_lines.remove(line)


    def can_allocate(self, line:OrderLine):
        return all(
            [
                line.qty <= self.available_quantity,
                self.sku == line.sku
            ]
        )
    def can_deallocate(self, line:OrderLine):
        return line in self._allocated_lines

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocated_lines)

    @property
    def available_quantity(self) -> int:
        return self._purchased_qty - self.allocated_quantity


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    print(sorted(batches))
    batch = next(
        b for b in sorted(batches) if b.can_allocate(line)
    )
    batch.allocate(line)
    return batch.reference


