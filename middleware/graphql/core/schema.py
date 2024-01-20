import graphene
from ..common.schema import ResultBase,BaseResultCode
from ..common.scalar import ObjectField

class ResultCommand(ResultBase):
	data = graphene.Field(ObjectField)

class Command(graphene.ObjectType):
	name = graphene.String()
	title = graphene.String()
	tooltip = graphene.String()
	args = graphene.List(ObjectField)

class Config(graphene.ObjectType):
	command = graphene.List(Command)
	document = graphene.List(graphene.String)
	object = graphene.List(graphene.String)
	property = graphene.List(graphene.String)