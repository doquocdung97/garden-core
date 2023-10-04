import graphene
from ..property.schema import ParentProperty
class Object(ParentProperty):
		uuid = graphene.UUID()
		name = graphene.String()
		label = graphene.String()
		type = graphene.String()
		