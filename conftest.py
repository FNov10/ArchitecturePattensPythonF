# pytest: disable=redefined-outer-name
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm import start_mappers

from db_tables import metadata


@pytest.fixture(scope='session')
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture(scope='session')
def session(in_memory_db):
    yield sessionmaker(bind=in_memory_db)()
