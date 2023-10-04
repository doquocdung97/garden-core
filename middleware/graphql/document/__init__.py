import graphene
from .schema import Document
from core import Core
class __Query(graphene.ObjectType):
	documents = graphene.Field(
			graphene.List(Document),
	)
	document = graphene.Field(
			Document,
			name = graphene.Argument(graphene.String, required=True),
	)
	
	def resolve_documents(self, info):
		return []
	def resolve_document(self, info,name):
		doc = Core.get(name)
		if doc:
			return doc.toJSON()
		# return doc
		
		
class __Mutation(graphene.ObjectType):
	test = graphene.Field(
			Document,
	)

schema = graphene.Schema(
		query=__Query,
		mutation=__Mutation
)
print(schema)