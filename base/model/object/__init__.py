from sqlalchemy import create_engine, Column, Integer, String,ForeignKey
import uuid
from ..database import  get_declarative_base,create_db_engine
from ..common import TimestampMixin
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from typing import Optional,List
from sqlalchemy.orm import backref
from ..tablename import OBJECT_TABLE,PROPERTY_TABLE
import enum

Base = get_declarative_base()
class OBJECTENUM:
    DOCUMENT    = "DOCUMENT"
    OBJECT      = "OBJECT"
    MEDIA       = "MEDIA"
    
class ObjectModel(TimestampMixin,Base):
    __tablename__ = OBJECT_TABLE.NAME
    __table_args__ = {'extend_existing': True}
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50))
    label = Column(String(50))
    version = Column(String(50))
    type:Mapped[OBJECTENUM] = Column(String(10),default=OBJECTENUM.OBJECT)
    parent_id = Column(Integer, ForeignKey(f"{OBJECT_TABLE.NAME}.{OBJECT_TABLE.ID}"))  # Self-referential FK
    kind = Column(String(50))
    # One-to-many
    children: Mapped[List[lambda:ObjectModel]] = relationship(
        lambda:ObjectModel,
        back_populates=OBJECT_TABLE.PARENT,
        cascade="all, delete-orphan"
    )

    # Many-to-one
    parent:Mapped[lambda:ObjectModel] = relationship(
        lambda:ObjectModel,
        back_populates=OBJECT_TABLE.CHILDREN,
        remote_side=[id]  # 👈 necessary for self-referential relationship
    )
    property: Mapped[List[lambda:PropertyModel]]  = relationship(lambda:PropertyModel, back_populates=PROPERTY_TABLE.OBJECT, cascade="all, delete-orphan")

    def __str__(self):
        obj = "Object"
        if self.type is OBJECTENUM.DOCUMENT:
            obj = "Document"
        return f"{obj}({self.name},{self.id})"
    
    def toJson(self):
        return  {
			"name":self.name,
			"version":self.version,
			"type":self.kind,
			'uuid':self.id,
		}
from ..property import PropertyModel