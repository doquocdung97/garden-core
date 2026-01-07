# from sqlalchemy import create_engine, Column, Integer, String
# import uuid
# from ..database import  get_declarative_base,create_db_engine
# from ..common import TimestampMixin

# from sqlalchemy.orm import declarative_base, sessionmaker, relationship
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import relationship
# from typing import Optional,List
# from sqlalchemy.orm import backref
# from ..tablename import OBJECT_TABLE,DOCUMENT_TABLE
# Base = get_declarative_base()

# class Document(TimestampMixin,Base):
#     __tablename__ = DOCUMENT_TABLE.NAME
#     __table_args__ = {'extend_existing': True}
#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = Column(String)
#     label = Column(String)
#     objects: Mapped[List[lambda:Object]]  = relationship(lambda:Object, back_populates=OBJECT_TABLE.DOCUMENT, cascade="all, delete-orphan")

# from ..object import Object

