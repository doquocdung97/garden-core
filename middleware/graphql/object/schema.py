import graphene
from ..property.schema import ParentProperty,Property
class Object(ParentProperty):
		uuid = graphene.UUID()
		name = graphene.String()
		label = graphene.String()
		type = graphene.String()
		

class ObjectObserver(graphene.ObjectType):
	name = graphene.String()
	property = graphene.Field(Property)