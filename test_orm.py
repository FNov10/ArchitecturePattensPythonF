from datetime import date
from model import Batch, OrderLine

def test_orderline_mapper_can_add_lines(session):
    session.execute(
        'INSERT INTO order_lines (orderid, sku, quantity) VALUES '
        '("order1", "RED-CHAIR", 12)')
    expected = [
        OrderLine("order1", "RED-CHAIR", 12)
    ]
    assert session.query(OrderLine).all() == expected

def test_orderline_mapper_can_save_lines(session):
    new_line = OrderLine("order12", "RED-CHAIR", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute('SELECT orderid, sku, qty from "order_lines'))
    assert rows == [('order12', 'RED-CHAIR', 12)]

