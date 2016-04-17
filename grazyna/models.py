from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, UniqueConstraint
from sqlalchemy.sql.sqltypes import Integer, DateTime, String

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=func.now())
    channel = Column(String(30), nullable=False, index=True)
    key = Column(String(20), nullable=False, index=True)
    message = Column(String(200), nullable=False)
