import graphene
from ..property.schema import ParentProperty,Property
from constants import VARIATIONS

class ObjectModeEnum(graphene.Enum):
	OBJECT = VARIATIONS.OBJECT
	MEDIA = VARIATIONS.MEDIA
	PARAMETER = VARIATIONS.PARAMETER

class Object(ParentProperty):
	uuid = graphene.UUID()
	name = graphene.String()
	label = graphene.String()
	type = graphene.String()
		

class ObjectObserver(graphene.ObjectType):
	name = graphene.String()
	uuid = graphene.UUID()
	property = graphene.Field(Property)