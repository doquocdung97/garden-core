import graphene,redis,asyncio,json
from typing import Any
from ..property.schema import Property
from .schema import ObjectObserver,Object,ObjectModeEnum
from ..common.scalar import ObjectField
from core import Core
from ...redis import ObserverGraphql
class _Query(graphene.ObjectType):
	objects = graphene.Field(graphene.List(Object),
													namedoc=graphene.Argument(graphene.String,required=True),
													nameobjects=graphene.Argument(graphene.List(graphene.String)))
	object = graphene.Field(Object,
													namedoc=graphene.Argument(graphene.String,required=True),
													nameobject=graphene.Argument(graphene.String,required=True),
													mode=graphene.Argument(ObjectModeEnum,required=True))
	
	objectChildren = graphene.Field(graphene.List(Object),
													namedoc=graphene.Argument(graphene.String,required=True),
													nameobject=graphene.Argument(graphene.String,required=True))
	
	def resolve_object(root, info,namedoc, nameobject,mode):
		doc = Core.get(namedoc)
		if doc:
			mode = doc.getMode(mode)
			obj = mode.getObjectByName(nameobject)
			if obj:
				return obj.toJSON()
		return None
	
	def resolve_objects(root, info,namedoc, nameobjects = None):
		doc = Core.get(namedoc)
		if doc:
			objs = []
			if nameobjects:
				for nameobject in nameobjects:
					obj = doc.getObjectByName(nameobject)
					if obj:
						objs.append(obj.toJSON())
			else:
				for obj in doc.Objects:
					objs.append(obj.toJSON())
			return objs
		return None
	
	def resolve_objectChildren(root, info,namedoc, nameobject = None):
		doc = Core.get(namedoc)
		if doc:
			objs = []
			obj = doc.getObjectByName(nameobject)
			if obj:
				for child in obj.OutListView:
					objs.append(child.toJSON())
			return objs
		return None
class _Mutation(graphene.ObjectType):
	createObject = graphene.String()
	deleteObject = graphene.String()
	
class _Subscription(graphene.ObjectType):
		propertyByObjectRealtime = graphene.Field(ObjectField,
																		namedoc=graphene.Argument(graphene.String,required=True),
																		nameobject=graphene.Argument(graphene.String,required=True),
																		nameproperty=graphene.Argument(graphene.String,required=True),
																		time=graphene.Argument(graphene.Float,required=True))
		
		propertysByObjectRealtime = graphene.Field(graphene.List(Property),
																		namedoc=graphene.Argument(graphene.String,required=True),
																		nameobject=graphene.Argument(graphene.String,required=True),
																		namepropertys=graphene.Argument(graphene.List(graphene.String),required=True),
																		time=graphene.Argument(graphene.Float,required=True))
		
		objectObserver = graphene.Field(ObjectObserver,
																		namedoc=graphene.Argument(graphene.String,required=True),
																		nameobject=graphene.Argument(graphene.String,required=True))
	
		def resolve_objectObserver(root, info,namedoc, nameobject):
			pubsub = ObserverGraphql.PubSubDoc(namedoc,f"{namedoc}_{nameobject}")
			if not pubsub:
				raise ValueError("not fount name document")
			subscription_uuid = info.context.get("subscription_uuid")
			info.context[f"subscription_pubsub_{subscription_uuid}"] = pubsub
			return pubsub._data_observer.map(lambda message: message)
		
		async def resolve_propertyByObjectRealtime(root, info,namedoc,nameobject,nameproperty,time):
			try:
				doc = Core.get(namedoc)
				if doc:
					obj = doc.getObjectByName(nameobject)
					if obj:
						property = obj.getProperty(nameproperty)
						if property:
							while True:
								yield property.getValue()
								await asyncio.sleep(time)
						raise ValueError("Not found Property by name: {nameproperty}")
					raise ValueError("Not found Object by name: {nameobject}")
				raise ValueError("Not found Document by name: {namedoc}")
			except asyncio.CancelledError as ex:
					raise ValueError(ex)
			
		async def resolve_propertysByObjectRealtime(root, info,namedoc,nameobject,namepropertys,time):
			try:
				doc = Core.get(namedoc)
				if doc:
					obj = doc.getObjectByName(nameobject)
					if obj:
						while True:
							propertys = []
							for nameproperty in namepropertys:
								property = obj.getProperty(nameproperty)
								if property:
									propertys.append(property.toJSON())
							yield propertys
							await asyncio.sleep(time)
					raise ValueError("Not found Object by name: {nameobject}")
				raise ValueError("Not found Document by name: {namedoc}")
			except asyncio.CancelledError as ex:
					raise ValueError(ex)

schema_object = graphene.Schema(
		query=_Query,
		mutation=_Mutation,
		subscription=_Subscription
)