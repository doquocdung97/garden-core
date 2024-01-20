import graphene,redis,asyncio,json
from typing import Any
from .schema import Document,DocumentObserver,Property
from ..common.scalar import ObjectField
from core import Core
from ...redis import ObserverGraphql
from ..common.scalar import ObjectField
class _Query(graphene.ObjectType):
	documents = graphene.Field(
			graphene.List(Document),
	)
	document = graphene.Field(
			Document,
			name = graphene.Argument(graphene.String, required=True),
	)
	documentTree = graphene.Field(
			ObjectField,
			namedoc = graphene.Argument(graphene.String, required=True),
			nameobject = graphene.Argument(graphene.String),
	)
	
	def resolve_documents(self, info):
		return []
	
	def resolve_documentTree(self, info, namedoc, nameobject = None):
		doc = Core.get(namedoc)
		if doc:
			if nameobject:
				obj = doc.getObjectByName(nameobject)
				if obj:
					return obj.tree_view(False)
				else:
					return None
			return doc.tree_view()
		return None
	
	def resolve_document(self, info,name):
		doc = Core.get(name)
		if doc:
			return doc.toJSON()
		
class _Mutation(graphene.ObjectType):
	test = graphene.Field(
			Document,
	)
	hello = graphene.String(text=graphene.Argument(graphene.String))
	def resolve_hello(root, info,text):
		# pubsub.punsubscribe("test")
		# pubsub.on_next(text)
		pass
class _Subscription(graphene.ObjectType):
		documentObserver = graphene.Field(DocumentObserver,name=graphene.Argument(graphene.String,required=True))

		def resolve_documentObserver(root, info,name):
			pubsub = ObserverGraphql.PubSubDoc(name)
			if not pubsub:
				raise ValueError("not fount name document")
			subscription_uuid = info.context.get("subscription_uuid")
			info.context[f"subscription_pubsub_{subscription_uuid}"] = pubsub
			return pubsub._data_observer.map(lambda message: message)
		
schema_document = graphene.Schema(
		query=_Query,
		mutation=_Mutation,
		subscription=_Subscription
)
# from graphql import GraphQLObjectType, GraphQLSchema, GraphQLString

# SubscriptionType = GraphQLObjectType(
#     name="Subscription",
#     fields={
#         "someSubscription": {
#             "type": GraphQLString,
#             "resolve": lambda root, info, **kwargs: subscription_resolver(root, info, info.context.get("subscription_id"), **kwargs)
#         }
#     }
# )
# schema = GraphQLSchema(
#     subscription=SubscriptionType
# )
