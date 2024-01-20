import graphene
from ..property.schema import ParentProperty,Property
from ..object.schema import Object,ObjectObserver
class Document(ParentProperty):
	uuid = graphene.UUID()
	name = graphene.String()
	label = graphene.String()
	version = graphene.String()
	type = graphene.String()
	parameters = graphene.Field(graphene.List(Property))
	objects = graphene.Field(graphene.List(Object))

class DocumentObserver(graphene.ObjectType):
	name = graphene.String()
	event = graphene.String()
	object = graphene.Field(ObjectObserver)
	property = graphene.Field(Property)
	parameter = graphene.Field(Property)
    