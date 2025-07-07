from ..object import ObjectModel
from sqlalchemy import Column, Integer, String, JSON
import uuid
from ..database import get_declarative_base, create_db_engine
from ..common import TimestampMixin
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional, List
from ..tablename import OBJECT_TABLE, PROPERTY_TABLE
from sqlalchemy.orm import Mapped

Base = get_declarative_base()


class PropertyModel(TimestampMixin, Base):
	__tablename__ = 'db_property'
	id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	name = Column(String(50))
	type = Column(String(50))
	group = Column(String(50))
	description = Column(String(500))
	status = Column(Integer)
	value = Column(JSON)
	attribute = Column(JSON)
	object_id = Column(Integer, ForeignKey(
		f"{OBJECT_TABLE.NAME}.{OBJECT_TABLE.ID}"))  # Self-referential FK
	object: Mapped[lambda:ObjectModel] = relationship(
		lambda: ObjectModel,
		back_populates=OBJECT_TABLE.PROPERTY
	)

	def __str__(self):
		return f"Property({self.name},{self.value})"

	def toJson(self):
		return {
			'name': self.name,
			'type': self.type,
			'value': self.value,
			'group': self.group,
			'description': self.description,
			'status': self.status,
			'attribute': self.attribute
		}
