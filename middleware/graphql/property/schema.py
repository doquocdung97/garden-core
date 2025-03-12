import graphene
from ..common.scalar import ObjectField
from ..common.schema import ResultBase
				
# class PropertyBase(graphene.ObjectType):
# 	name = graphene.String()
# 	description = graphene.String()
# 	status = graphene.Int()
# 	type = graphene.String()
# 	value = graphene.Field(ObjectField)
# 	attribute = graphene.Field(ObjectField)
	
# class PropertyEnum(PropertyBase):
# 	values = graphene.Field(graphene.List(ObjectField))
		 
# class Property(graphene.Union):
# 		class Meta:
# 				types = (PropertyBase,PropertyEnum)
# 		@classmethod
# 		def resolve_type(cls, data, info):
# 			type = data.get("type")
# 			if "Enum" in type:
# 				return PropertyEnum
# 			return PropertyBase
class PropertyStatusEnum(graphene.Enum):
	FULL = 1
	ONLYVIEW = 2

class Property(graphene.ObjectType):
	name = graphene.String()
	description = graphene.String()
	status = graphene.Field(PropertyStatusEnum)
	type = graphene.String()
	value = graphene.Field(ObjectField)
	attribute = graphene.Field(ObjectField)

class ParentProperty(graphene.ObjectType):
	propertys = graphene.List(Property)

class InputProperty(graphene.InputObjectType):
	type = graphene.Field(graphene.String,required=True)
	name = graphene.Field(graphene.String,required=True)
	description = graphene.String()
	status = graphene.Field(PropertyStatusEnum,default_value=PropertyStatusEnum.FULL)
	# value = graphene.Field(ObjectField,required=True)
	attribute = graphene.Field(ObjectField)
	group = graphene.String()

class PropertyResultBase(ResultBase):
	data = graphene.Field(Property)