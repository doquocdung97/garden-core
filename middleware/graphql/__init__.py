import graphene
from .document import schema 

class Query(schema.query):
	pass

class Mutation(schema.mutation):
	pass

schema = graphene.Schema(
		query=Query,
		mutation=Mutation
)