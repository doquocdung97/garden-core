import graphene,redis,asyncio,json
from typing import Any
from .schema import Media
from ..common.scalar import ObjectField
from core import Core
from ...redis import ObserverGraphql

class _Query(graphene.ObjectType):
	medias = graphene.Field(
			graphene.List(Media),
			name=graphene.Argument(graphene.String,required=True)
	)

	def resolve_medias(self, info,name):
		doc = Core.get(name)
		if doc:
			return doc.Media.toJSON()
		return None
	
class _Mutation(graphene.ObjectType):
	createMedia = graphene.Field(Media,doc=graphene.Argument(graphene.String))
	def resolve_hello(root, info,text):
		pass
		
schema_media = graphene.Schema(
		query=_Query,
		mutation=_Mutation
)