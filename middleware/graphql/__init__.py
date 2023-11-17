import graphene,asyncio
from .document import schema_document
from .object import schema_object
from ..redis import ObserverGraphql

def merge_schema(*args):
	schema = graphene.Schema()
	query = []
	mutation = []
	subscription = []
	for schema in args:
		if isinstance(schema,graphene.Schema):
			if schema._query:
				query.append(schema._query)
			if schema._mutation:
				mutation.append(schema._mutation)
			if schema._subscription:
				subscription.append(schema._subscription)

	class Query(*query):
		pass

	class Mutation(*mutation):
			pass
	# def MergeSchema()
	if not ObserverGraphql.IsOpenRedis:
		return graphene.Schema(
			query=Query,
			mutation=Mutation
		)
	class Subscription(*subscription):
			pass

	return graphene.Schema(
			query=Query,
			mutation=Mutation, 
			subscription=Subscription
	)

schema = merge_schema(schema_document,schema_object)