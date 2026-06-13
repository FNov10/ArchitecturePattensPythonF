from idlelib.sidebar import LineNumbers

from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy import Table, Column, String, Integer, MetaData, select, create_engine
import model

metadata = MetaData()

order_lines = Table(
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', String(255)),
    Column('orderid', String(255))
)

def start_mappers():
    lines_mapper = mapper(model.OrderLine, order_lines)
    print(lines_mapper)



start_mappers()

# 1. Initialize the Engine
engine = create_engine("sqlite:///example.db")
metadata.create_all(engine)
# 2. Create a configurable Session factory
session = Session(engine)
new_line = model.OrderLine("order1", "RED-CHAIR", 12)
session.add(new_line)
session.commit()
rows = list(session.execute('SELECT * from order_lines'))
print(rows)

