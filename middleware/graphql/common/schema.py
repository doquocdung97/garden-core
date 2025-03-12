import graphene

class BaseResultCode(graphene.Enum):
	B000 = 0
	B001 = 1
	B002 = 2
	B003 = 3
	B004 = 4
	B005 = 5

class ResultBase(graphene.ObjectType):
	code = graphene.Field(BaseResultCode,default_value=BaseResultCode.B000)
	success = graphene.Boolean(default_value=True)
	message = graphene.String()