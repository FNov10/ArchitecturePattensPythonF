from datetime import date, timedelta
import pytest
from model import *

# from model import ...

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def make_batch_and_line(sku: str, batch_qty: int, line_qty:int):
    return (
        Batch("batch_001", sku, batch_qty, today),
        OrderLine("order-001", line_qty, sku)
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    test_batch = Batch("batch_001", "BigTable", 30, later)
    test_orderline = OrderLine(
        "sample-order",
        6,
        "BigTable",
    )
    print(f"Assigning orderline of {test_orderline.qty} to {test_batch}")
    test_batch.allocate(test_orderline)
    print(f"Batch is now: {test_batch}")
    assert test_batch.available_quantity == 24


def test_can_allocate_if_available_greater_than_required():
    test_batch, test_orderline = make_batch_and_line(
        "Lamp", 30,  20
    )
    assert test_batch.can_allocate(test_orderline)


def test_cannot_allocate_if_available_smaller_than_required():
    test_batch, test_orderline = make_batch_and_line(
        "Lamp", 30, 40
    )
    assert not test_batch.can_allocate(test_orderline)


def test_can_allocate_if_available_equal_to_required():
    test_batch, test_orderline = make_batch_and_line(
        "Lamp", 40, 40
    )
    assert test_batch.can_allocate(test_orderline)

def test_cannot_allocate_if_skus_do_not_match():
    test_batch = Batch("batch_001", "BigTable", 30, later)
    test_orderline = OrderLine(
        "sample-order",
        6,
        "BigChair",
    )
    assert test_batch.can_allocate(test_orderline) is False


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("TABLE", 40, 30)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 40

def test_allocation_is_impodent():
    batch, line = make_batch_and_line("TABLE", 40, 30)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity==10



def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


def test_prefers_earlier_batches():
    pytest.fail("todo")
