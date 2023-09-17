import graphene
from ..common.scalar import ObjectField

class Human(graphene.ObjectType):
		name = graphene.String()
		born_in = graphene.String()

class Droid(graphene.ObjectType):
		name = graphene.String()
		primary_function = graphene.String()

class Starship(graphene.ObjectType):
		name = graphene.String()
		length = graphene.Int()


class ValueUnion(graphene.Union):
		class Meta:
				types = (Human, Droid, Starship)
				
class PropertyBase(graphene.ObjectType):
	name = graphene.String()
	description = graphene.String()
	status = graphene.Int()
	type = graphene.String()
	value = graphene.Field(ObjectField)
	# tip = graphene.String()
	
class PropertyEnum(PropertyBase):
	values = graphene.Field(graphene.List(ObjectField))
		 
class Property(graphene.Union):
		class Meta:
				types = (PropertyBase,PropertyEnum)
		@classmethod
		def resolve_type(cls, data, info):
			type = data.get("type")
			if "Enum" in type:
				return PropertyEnum
			return PropertyBase
				
class ParentProperty(graphene.ObjectType):
	propertys = graphene.List(Property)