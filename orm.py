from idlelib.sidebar import LineNumbers

from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy import Table, Column, String, Integer, MetaData, select, create_engine, Date, ForeignKey
import model

metadata = MetaData()

order_lines = Table(
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', String(255)),
    Column('orderid', String(255))
)

batches = Table(
    'batches', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reference', String(255)),
    Column('sku', String(255)),
    Column('_purchased_quantity', Integer, nullable=False),
    Column('eta',Date, nullable=True)
)

allocations = Table(
    'allocations', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('orderline_id', Integer, ForeignKey('order_lines.id')),
    Column('batch_id', Integer, ForeignKey('batches.id'))
)


def start_mappers():
    # The relationship between Batch and OrderLine is many-to-many, using the
    # `allocations` table as an intermediary link (a "secondary" table).
    # This schema is intentionally flexible:
    #  - A single batch can fulfill many different order lines.
    #  - A single large order line can be fulfilled by multiple smaller batches.
    #
    # Even though the current business logic in `model.py` only implements a
    # simple "all-or-nothing" allocation from a batch, this database structure
    # is robust. It allows us to evolve the domain logic to handle more complex
    # scenarios (like splitting orders) in the future without needing to change
    # the database schema itself.
    lines_mapper = mapper(model.OrderLine, order_lines)
    mapper(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper, secondary=allocations, collection_class=set,
            )
        },
    )


start_mappers()

# 1. Initialize the Engine
engine = create_engine("sqlite:///example2.db")
metadata.create_all(engine)
# 2. Create a configurable Session factory
session = Session(engine)
new_line = model.OrderLine("order1", "RED-CHAIR", 12)
test_batch = model.Batch('batch-001','RED-CHAIR',100, None)
# session.add(test_batch)
# session.commit()
# rows = list(session.execute('SELECT * from batches'))
# print(next(batch for batch in session.query(model.Batch).all() if batch.reference=="bruh" else None))
# print(rows)
session.close()
