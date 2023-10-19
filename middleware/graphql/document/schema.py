import graphene
from ..property.schema import ParentProperty,Property
from ..object.schema import Object
class Document(ParentProperty):
		uuid = graphene.UUID()
		name = graphene.String()
		label = graphene.String()
		version = graphene.String()
		type = graphene.String()
		objects = graphene.Field(graphene.List(Object))
		
class ObjectObserver(graphene.ObjectType):
	name = graphene.String()
	property = graphene.Field(Property)

class DocumentObserver(graphene.ObjectType):
	name = graphene.String()
	event = graphene.String()
	object = graphene.Field(ObjectObserver)
	property = graphene.Field(Property)
    