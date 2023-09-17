import graphene
from ..property.schema import ParentProperty
from ..object.schema import Object
class Document(ParentProperty):
		uuid = graphene.UUID()
		name = graphene.String()
		label = graphene.String()
		version = graphene.String()
		type = graphene.String()
		objects = graphene.Field(graphene.List(Object))
		