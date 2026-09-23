from abc import ABC, abstractmethod
from typing import Optional
from model import *

class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> Optional[Batch]:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference) -> Optional[Batch]:
        return self.session.query(Batch).filter_by(reference=reference).one()


class SqlRepositoryNoORM(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get(self, reference) -> Batch:
        [(id, ref, sku, qty, eta)] = list(self.session.execute(
            'SELECT id, reference, sku, _purchased_quantity, eta FROM batches WHERE reference=:batch_id',
            dict(batch_id=reference)),
        )
        batch = Batch(ref, sku, qty, eta)
        [[orderline_id]] = list(self.session.execute(
            'SELECT orderline_id FROM allocations WHERE batch_id=:batch_id',
            dict(batch_id=id)
        ))
        [(orderid, sku, qty)] = list(self.session.execute(
            'SELECT orderid, sku, qty from order_lines WHERE id=:id',
            dict(id=orderline_id)))

        batch.allocate(OrderLine(orderid, sku, qty))

        return batch

    def add(self, batch):
        batch_id = batch.reference
        batch_allocations = batch._allocations
        batch_purchased = batch._purchased_quantity
        batch_eta = batch.eta
        batch_sku = batch.sku
        self.session.execute(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
            ' VALUES (:batch_id, :batch_sku, :batch_purchased, :batch_eta)',
            dict(batch_id=batch_id, batch_sku=batch_sku, batch_purchased=batch_purchased, batch_eta
                 =batch_eta),
        )
        for allocation in batch_allocations:
            line_id = allocation.orderid
            self.session.execute(
                "INSERT INTO allocations (orderline_id, batch_id)"
                " VALUES (:orderline_id, :batch_id)",
                dict(orderline_id=line_id, batch_id=batch_id),
            )


        