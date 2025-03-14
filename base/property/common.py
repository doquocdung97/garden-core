from common import group_duplicates,createAttribute
from  inspect import ismethod,isfunction
from constants import VARIATIONS

class PropertyBase:
		def __init__(self, obj, name, group, description, status, type,attribute = {}):
				self.object = obj
				self.__Name = name
				self.__type = type
				self.group = group
				self.description = description
				self.status = status
				if not attribute:
					attribute = {}
				self.attribute = attribute
				self.__Value = self.valueDefault()
				self.__parameter = None

		def valueDefault(self):
				return None
		
		def getName(self):
			return self.__Name
		
		@property
		def Value(self):
			return self.getValue()

		@Value.setter
		def Value(self, value):
				val = value
				from ..parameter import PropertyParameter
				if isinstance(val,PropertyParameter):
					val = val.getValue()
				if self.checkValue(val):
						if isinstance(value,PropertyParameter):
							self.__parameter = value
							value.addInList(self)
							self.object.onBeforeChange(self.__Name)
							self.setValue(val)
							self.onChange()
						elif self.getValue() != val:
								self.__parameter = None
								self.object.onBeforeChange(self.__Name)
								self.setValue(val)
								self.onChange()
								# self.object.setChange(True)
				else:
						raise ValueError('not value type')
		def onChange(self):
			self.object.onChanged(self.__Name)
			from base.object import ObjectBase
			if isinstance(self.object,ObjectBase):
				self.object.Document.onChangedObject(self.object,self.__Name)

		def getType(self):
				return self.__class__.__name__

		def save(self):
			data = {
					'name': self.__Name,
					'type': self.__type,
					'group': self.group,
					'description': self.description,
					'status': self.status,
					'attribute':self.attribute
			}

			parameter = self.__parameter
			if parameter:
				data["parameter"] = parameter.toString()
			else:
				data["value"] = self.getValue(True)

			return data
		
		def toJSON(self):
			return {
					'name': self.__Name,
					'type': self.__type,
					'value': self.getValue(),
					'group': self.group,
					'description': self.description,
					'status': self.status,
					'attribute':self.attribute
			}
		
		def convert(self,val):
				return val

		def restore(self, reader:dict):
				val = None
				if reader.get('parameter'):
					try:
						from base.object import ObjectBase
						if isinstance(self.object,ObjectBase):
							self.__parameter = eval(f"self.object.Document.{reader['parameter']}")
							self.__parameter.addInList(self)
							val = self.__parameter.getValue()
					except:
						pass
				else:
					val = self.convert(reader['value'])
				self.setValue(val)
				pass

		def getValue(self, isSave=False):
				if self.__parameter:
					return self.__parameter.getValue(isSave)
				return self.__Value

		def checkValue(self, val):
				return True

		def setValue(self, val):
				self.__Value = val

		def toString(self):
				return self.__Value

		def __repr__(self):
				return str(f'{self.__class__.__name__}({self.toString()})')
		#     return self
		def clone(self):
			pro = self.__class__(self.object,self.__Name,self.group,self.description,self.status,self.__type,self.attribute)
			pro.__parameter = self.__parameter
			try:
				pro.Value = self.Value
			except:
				pass
			return pro

def PropertyListBase(target):
		name = f'{target.__name__}s'
		class PropertyListBase(target):
				def valueDefault(self):
						return []
				
				def getType(self):
					return name
				
				def checkValue(self, vals:list):
						if isinstance(vals,list):
								for val in vals:
										if not super(PropertyListBase,self).checkValue(val):
												return False
								return True
						return False
				def convert(self, vals):
						datas = []
						for val in vals:
							data = super(PropertyListBase,self).convert(val)
							if data:
								datas.append(data)
						return datas
		
				def __repr__(self):
						# val = super(PropertyListBase,self).toString()
						return str(f'{name}({self.getValue()})')

		return PropertyListBase

def PropertyEnumBase(target):
		name = f'{target.__name__}Enum'
		class PropertyEnumBase(target):
				def checkValue(self,val):
						if ismethod(val) and self.object.__getattribute__(val.__func__.__name__) :
							return True
						elif isinstance(val,list):
								if val == self.getValues():
									raise ValueError("Not change data")
								for v in val:
										if not super(PropertyEnumBase,self).checkValue(v) or (isinstance(v,str) and not v):
												return False
								return True
						elif super(PropertyEnumBase,self).checkValue(val) and len(self.getValues()) > 0 and val in self.getValues():
								return True
						else:
								return False
				
				def toJSON(self):
					data = super(PropertyEnumBase,self).save()
					return data
				
				def getValue(self, isSave=False):
					if self.attribute.get("values_function"):
						self.attribute["values"] = self.object.__getattribute__(self.attribute["values_function"])(self)
					return super(PropertyEnumBase,self).getValue(isSave)

				def getValues(self):
						if not self.attribute or not self.attribute.get("values"):
							return []
						if self.attribute.get("values_function"):
							return self.object.__getattribute__(self.attribute["values_function"])(self)
						return self.attribute["values"]
				
				def setValue(self, val):
						if ismethod(val) or isfunction(val):
							self.attribute["values_function"] = val.__func__.__name__
							self.attribute["values"] = val(self)
							super(PropertyEnumBase,self).setValue(None)
						elif isinstance(val,list):
								self.attribute["values"] = group_duplicates(val)
								v = super(PropertyEnumBase,self).getValue()
								if v and not v in val:
										super(PropertyEnumBase,self).setValue(None)
						else:
								super(PropertyEnumBase,self).setValue(val)

				def __repr__(self):
						return str(f'{name}({self.toString()})')
				
				def restore(self, reader=None):
						self.setValue(reader['value'])

				def clone(self):
					pro = super(PropertyEnumBase,self).clone()
					if self.Value:
						pro.Value = self.Value
					else:
						pro.Value = pro.valueDefault()
					return pro

		return PropertyEnumBase

def PropertyViewBase(target):
	name = f'{target.__name__}View'
	class PropertyViewBase(target):
		@property
		def Value(self):
			return super(PropertyViewBase,self).Value
		
		def checkValue(self,val):
			if ismethod(val) or isfunction(val):
				return True
			
		@Value.setter
		def Value(self, val):
			self.func_value = val
		
		def save(self):
			data = super().save()
			del data['value']
			return data
		
		def getValue(self, isSave=False):
			# val = super(PropertyViewBase,self).getValue()
			if hasattr(self,'func_value') and (ismethod(self.func_value) or isfunction(self.func_value)):
				self.setValue(self.func_value())
				
			return super(PropertyViewBase,self).getValue(isSave)
		
		def toJSON(self):
			data = super().toJSON()
			data["value"] = self.getValue(True)
			return data
		
		def __repr__(self):
			return str(f'{name}({self.toString()})')
		
	return PropertyViewBase

class MainProperty():
		instance = None
		properties = {}

		def __init__(self):
				# super().__init__()
				if (MainProperty.instance):
						self = MainProperty.instance
				else:
						MainProperty.instance = self

		def get(self, name: str = None) -> list[PropertyBase] | PropertyBase | None:
				if not name:
						return self.properties
				return self.properties.get(name)
		# def get(self)->list[PropertyBase]:
		#     return self.properties
		
		def add(self, property: type,isList:bool = False, isEnum:bool = False, isView:bool = False) -> bool:
				name = property.__name__
				if issubclass(property, PropertyBase):
						datas = [
								(name,property)
						]
						if isList:
								datas.append((f'{name}s',PropertyListBase(property)))
						if isEnum:
								datas.append((f'{name}Enum',PropertyEnumBase(property)))
						if isView:
							datas.append((f'{name}View',PropertyViewBase(property)))
						for item in datas:
								if not item[0] in self.properties:
										self.properties[item[0]] = item[1]
						return True
				return False
		
class HanlderProperty:
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.__propertys = []
			self.__out_list_view = []
			self.__in_list_view = []
	
		@property
		def OutListView(self):
			return self.__out_list_view
		@property
		def InListView(self):
			return self.__in_list_view
		
		def isInit(self):
			return True
		
		@property
		def propertys(self)->list[str]:
			return self.__propertys
		
		def getProperty(self,name:str)->PropertyBase|None:
			if name in self.__propertys:
				property = self.__dict__.get(name)
				return property
		
		def addProperty(self,type:str,name:str,group:str = '',description:str = '',status:int = 1,attribute = {})->PropertyBase|None:
				mainProperty = MainProperty()
				property = mainProperty.get(type)
				if property:
						name = createAttribute(self,name)
						property = property(self,name,group,description,int(status),type,attribute)
						self.__dict__[name] = property
						self.__propertys.append(name)
						return property
				return None
		
		def restoreProperty(self,reader):
			for property in reader:
				try:
					self.addProperty(property['type'],property['name'],property['group'],property['description'],property['status'],property['attribute'])
					if property['name'] in self.propertys:
						self.__dict__[property['name']].restore(property)
						self.__update_in_and_out_list(property['type'],self.__dict__[property['name']].Value)
				except Exception as ex:
					pass

		def saveProperty(self):
			parameters = []
			for property in self.__propertys:
				dataproperty = self.__dict__[property].save()
				parameters.append(dataproperty)
			return parameters

		def toJSONProperty(self):
			parameters = []
			for property in self.__propertys:
				dataproperty = self.__dict__[property].toJSON()
				parameters.append(dataproperty)
			return parameters

		def checkNameInProperty(self,name:str)->bool:
			return (name in self.__propertys)
		
		def get_command(self)->list[str]:
			return []
		
		def get_type(self)->str:
			return self.__class__.__name__
		
		def tree_view(self, check_in_list = True):
			if len(self.InListView) > 0 and check_in_list:
				return
			
			children = []
			for obj in self.__out_list_view:
				children.append(obj.tree_view(False))

			data = {
				'uuid':self.UUID,
				'type':self.__class__.__name__,
				'name':self.Name, 
				'theme': VARIATIONS.OBJECT,
				'children':children
			}
			return data
		
		def __update_in_and_out_list(self,type_name,value_new,value_old = None):
			if type_name in ["PropertyObjects"]:
				if value_old and len(value_old) > 0:
					for obj in value_old:
						self.__out_list_view.remove(obj)
						obj.__in_list_view.remove(self)
				if value_new and len(value_new) > 0:
					self.__out_list_view = self.__out_list_view + value_new
					for obj in value_new:
						obj.__in_list_view.append(self)

			if type_name in ["PropertyObject"]:
				if value_old:
					self.__out_list_view.remove(value_old)
					value_old.__in_list_view.remove(self)
				if value_new:
					self.__out_list_view.append(value_new)
					value_new.__in_list_view.append(self)
					
		def __setattr__(self, name, value):
			if hasattr(self,name) and name in self.__propertys:
				value_old = self.__dict__[name].Value
				self.__dict__[name].Value = value
				value_new = self.__dict__[name].Value
				type_name = self.__dict__[name].getType()
				self.__update_in_and_out_list(type_name,value_new,value_old)
				# if type_name in ["PropertyObjects"]:
				# 	if value_old and len(value_old) > 0:
				# 		for obj in value_old:
				# 			self.__out_list_view.remove(obj)
				# 			obj.__in_list_view.remove(self)
				# 	if value_new and len(value_new) > 0:
				# 		self.__out_list_view = self.__out_list_view + value_new
				# 		for obj in value_new:
				# 			obj.__in_list_view.append(self)

				# if type_name in ["PropertyObject"]:
				# 	if value_old:
				# 		self.__out_list_view.remove(value_old)
				# 		value_old.__in_list_view.remove(self)
				# 	if value_new:
				# 		self.__out_list_view.append(value_new)
				# 		value_new.__in_list_view.append(self)
				return
			return super(HanlderProperty,self).__setattr__(name, value)

		def __getattribute__(self, name):
			try:
				property =  super(HanlderProperty,self).__getattribute__(name)
				if isinstance(property,PropertyBase):
					return property.Value
			except:
				pass
			return super(HanlderProperty,self).__getattribute__(name)
		
		def _cloneProperty(self,target):
			for name in self.__propertys:
				try:
					pro = self.__dict__[name]
					pro = pro.clone()
					target.__dict__[name] = pro
					if not name in target.__propertys:
						target.__propertys.append(name)
				except:
					pass

		def onBeforeChange(self,prop):
			pass
		
		def onChanged(self, prop):
			pass
		
		def remove_object_from_property(self,obj):
			for pro in obj.propertys:
				property = obj.__dict__.get(pro)
				if property and property.getType() in ["PropertyObjects","PropertyObject"]:
					value = obj.__getattribute__(pro)
					if isinstance(value,list) and self in value:
						value = value.copy()
						value.remove(self)
						obj.__setattr__(pro,value)
					elif self == value:
						obj.__setattr__(pro,None)
						
		def __del__(self):
			for obj in [*self.OutListView]:
				obj.remove_object_from_property(self)
			for obj in [*self.InListView]:
				self.remove_object_from_property(obj)