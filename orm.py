from idlelib.sidebar import LineNumbers

from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy import Table, Column, String, Integer, MetaData, select, create_engine, Date, ForeignKey
from model import *
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

    """

    The mapper() function bridges your pure Python classes (Domain) with SQLAlchemy Table objects (Infrastructure). This is SQLAlchemy's classical/imperative mapping style.

    lines_mapper = mapper(OrderLine, order_lines)
    This binds the pure Python OrderLine class to the SQLAlchemy order_lines table. When you query the database, SQLAlchemy will return instances of OrderLine.

    mapper(Batch, batches, properties={...})
    This binds the pure Python Batch class to the batches table. The properties dictionary tells SQLAlchemy how to handle attributes that aren't simple database columns.

    "_allocations": relationship(...)
    This targets the private _allocations attribute on your Batch class and tells SQLAlchemy how to populate it using a relationship.

    lines_mapper
    The first argument to the relationship specifies the target of the relationship. It points to the OrderLine mapping defined in the first line.

    secondary=allocations
    This is the keyword that defines the many-to-many relationship. It tells SQLAlchemy to use the allocations table as the intermediary bridge to find which OrderLines belong to the Batch.

    collection_class=set
    By default, SQLAlchemy populates one-to-many or many-to-many relationships as Python list objects. This overrides that behavior, instructing SQLAlchemy to populate batch._allocations as a Python set. This ensures uniqueness and matches how the pure Python domain model expects to handle allocations.
    """
    lines_mapper = mapper(OrderLine, order_lines)
    mapper(
        Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper, secondary=allocations, collection_class=set,
            )
        },
    )


start_mappers()

# 1. Initialize the Engine
engine = create_engine("sqlite:///:memory:")
metadata.create_all(engine)
# 2. Create a configurable Session factory
session = Session(engine)
new_line = OrderLine("order1", "RED-CHAIR", 12)
test_batch = Batch('batch-001','RED-CHAIR',100, None)
test_batch.allocate(new_line)
print(test_batch.allocated_quantity)
session.add(test_batch)
session.commit()
rows = (session.execute('SELECT * from allocations'))
print(session.query(Batch).all())
print(rows)

session.execute(
        "INSERT INTO order_lines (orderid, sku, qty)"
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
# Nested iterable unpacking
orderline_id = list(session.execute(
    "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
    dict(orderid="order1", sku="GENERIC-SOFA"),
))



session.close()
