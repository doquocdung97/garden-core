import graphene
from ..property.schema import ParentProperty
from constants import VARIATIONS

class Media(ParentProperty):
  uuid = graphene.UUID()
  name = graphene.String()
  type = graphene.String()
  label = graphene.String()