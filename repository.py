from abc import ABC, abstractmethod
import model


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)
        self.session.commit()
        ...

    def get(self, reference) -> model.Batch:
        try:
         return next(batch for batch in self.session.query(model.Batch).all() if batch.reference == reference )
        except StopIteration:
         return None