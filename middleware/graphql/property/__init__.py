import graphene,redis,asyncio,json
from typing import Any
from .schema import Property
# from ..object.schema import ObjectObserver,Object
from ..common.scalar import ObjectField
from ..common.schema import ResultBase
from .schema import Property,InputProperty,PropertyResultBase
from ..object.schema import ObjectModeEnum
from core import Core
# from ...redis import ObserverGraphql
class _Query(graphene.ObjectType):
	test = graphene.String()
class _Mutation(graphene.ObjectType):
	deleteProperty = graphene.String()

	createParameter = graphene.Field(PropertyResultBase,
																  doc=graphene.Argument(graphene.String,required=True),
																	input=graphene.Argument(InputProperty,required=True))
	
	updateProperty = graphene.Field(PropertyResultBase,
																  namedoc=graphene.Argument(graphene.String,required=True),
													        nameobject=graphene.Argument(graphene.String),
																	nameproperty=graphene.Argument(graphene.String,required=True),
																	value=graphene.Argument(ObjectField,required=True),
																	mode=graphene.Argument(ObjectModeEnum,required=True),
																	parameter=graphene.Argument(graphene.Boolean,default_value=False))
	
	def resolve_updateProperty(root, info,namedoc,nameproperty,value,mode, nameobject = None,parameter = False):
		model = PropertyResultBase()
		try:
			doc = Core.get(namedoc)
			if doc:
				if nameobject:
					mode = doc.getMode(mode)
					obj = mode.getObjectByName(nameobject)
					if obj:
						pro = obj.getProperty(nameproperty)
						if pro:
							if pro.status == 2:
								raise TypeError("This value is read only")
							pro.Value = pro.convert(value)
							model.data = pro.toJSON()
							return model
						else:
							raise KeyError("not found property")
					else:
						raise KeyError("not found object")
				else:
					if parameter:
						pro = doc.Parameter.getProperty(nameproperty)
					else:
						pro = doc.getProperty(nameproperty)
					if pro:
						if pro.status == 2:
							raise TypeError("This value is read only")
						pro.Value = pro.convert(value)
						model.data = pro.toJSON()
						return model
					else:
						raise KeyError("not found property")
			else:
					raise KeyError("not found docuemnt")
		except Exception as ex:
			model.success = False
			model.code = 5
			model.message = str(ex)
		# 	return model
		# model.success = False
		# model.code = 2
		return model
	
	def resolve_createParameter(root, info,doc,input):
		model = PropertyResultBase()
		try:
			doc = Core.get(doc)
			if doc:
				parameter = doc.Parameter
				property = parameter.addProperty(
					type=input.type,
					name=input.name,
					group=input.group,
					status=input.status.value,
					attribute=input.attribute)
				# property.Value = input.value
				if property:
					model.data = property.toJSON()
					return model
		except Exception as ex:
			model.success = False
			model.code = 5
			return model
		model.success = False
		model.code = 2
		return model
	
schema_property = graphene.Schema(
		query=_Query,
		mutation=_Mutation,
)