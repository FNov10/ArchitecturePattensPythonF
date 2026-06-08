from datetime import date, timedelta
import pytest
from model import *

today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days = 10)

def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch(
        ref="in-stock-batch",
        sku="RETRO-CLOCK",
        qty=100,
        eta=None
    )
    shipment_batch = Batch(
        ref="shipment-batch",
        sku="RETRO-CLOCK",
        qty=100,
        eta=tomorrow
    )
    line = OrderLine(
        orderid="oref",
        sku="RETRO-CLOCK",
        qty=10
    )
    allocate(line,[in_stock_batch,shipment_batch])

    assert in_stock_batch.available_quantity==90
    assert shipment_batch.available_quantity==100