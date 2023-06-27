import datetime
import decimal
import threading
import uuid
from dataclasses import fields
from functools import wraps
from typing import Type, TypeVar, Generic, Iterator, Dict, Any

from sqlalchemy import Table, types, Column, create_engine
from sqlalchemy.orm import registry, sessionmaker, scoped_session
from sqlalchemy.sql.type_api import TypeEngine

import easy_pysy as ez

T = TypeVar('T')

mapper_registry = registry()
engine = create_engine("sqlite://", echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class Repository(Generic[T]):

    def __init__(self, type: Type[T]):
        self.type = type
        register_type(self.type)

    def get_by_id(self, id: str) -> T:
        return current_session().get(self.type, id)
            # query = select(self.type).where(id=id)
            # return session.scalars(query).one()

    def find_all(self) -> Iterator[T]:
        pass

    def save(self, value: T):
        session = current_session()
        session.add(value)
        session.commit()

    def delete_by_id(self, id: str):
        pass


type_map: Dict[Type[Any], TypeEngine[Any]] = {
    bool: types.Boolean(),
    bytes: types.LargeBinary(),
    datetime.date: types.Date(),
    datetime.datetime: types.DateTime(),
    datetime.time: types.Time(),
    datetime.timedelta: types.Interval(),
    decimal.Decimal: types.Numeric(),
    float: types.Float(),
    int: types.Integer(),
    str: types.String(),
    uuid.UUID: types.Uuid(),
}


def register_type(type: Type[T]):
    name = type.__name__
    columns = get_columns(type)
    table = Table(name, mapper_registry.metadata, *columns)
    mapper_registry.map_imperatively(type, table)


def get_columns(type: Type[T]):
    columns = []
    for field in fields(type):
        sqlalchemy_type = type_map[field.type]
        primary_key = field.name == 'id'
        column = Column(field.name, sqlalchemy_type, primary_key=primary_key)
        columns.append(column)
    return columns


@ez.on(ez.AppStarted)
def create_all(event: ez.AppStarted):
    mapper_registry.metadata.create_all(engine)


local = threading.local()


def current_session() -> Session:
    ez.require(hasattr(local, "session") and local.session is not None, "No session found, please use @ez.transactional")
    return local.session


def transactional():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with Session() as local.session:
                try:
                    return func(*args, **kwargs)
                except:
                    Session.rollback()
                    raise
                finally:
                    Session.remove()
                    local.session = None
        return wrapper
    return decorated
