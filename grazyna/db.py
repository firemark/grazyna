from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as BaseSession
from sqlalchemy.engine.reflection import Inspector

from .models import Base
from contextlib import contextmanager


class Session(BaseSession):

    @contextmanager
    def scope(self):
        "from http://docs.sqlalchemy.org/en/rel_1_0/orm/session_basics.html"
        try:
            yield self
            self.commit()
        except:
            self.rollback()
            raise
        finally:
            self.close()


def get_engine(uri):
    engine = create_engine(uri)
    inspector = Inspector.from_engine(engine)
    if not inspector.get_table_names():
        create_database(engine)
    return engine


def get_session(engine):
    return sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False
    )()


def create_database(engine):
    Base.metadata.create_all(engine)
