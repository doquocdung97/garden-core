from common import group_duplicates,createAttribute
class PropertyBase:
		def __init__(self, obj, name, group, description, status, type):
				self.object = obj
				self.__Name = name
				self.__type = type
				self.group = group
				self.description = description
				self.status = status
				self.__Value = self.valueDefault()

		def valueDefault(self):
				return None

		@property
		def Value(self):
				return self.getValue()

		@Value.setter
		def Value(self, val):
				if self.checkValue(val):
						if self.getValue() != val:
								self.object.onBeforeChange(self.__Name)
								self.setValue(val)
								self.object.onChanged(self.__Name)
								# self.object.setChange(True)
				else:
						raise ValueError('not value type')

		def getType(self):
				return self.__class__.__name__

		def save(self, reader=None):
				return {
						'name': self.__Name,
						'type': self.__type,
						'value': self.getValue(True),
						'group': self.group,
						'description': self.description,
						'status': self.status
				}
		def convert(self,val):
				return val

		def restore(self, reader=None):
				val = self.convert(reader['value'])
				self.setValue(val)
				pass

		def getValue(self, isSave=False):
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


def PropertyListBase(target):
		name = f'{target.__name__}s'
		class PropertyListBase(target):
				def valueDefault(self):
						return []

				def checkValue(self, vals:list):
						if isinstance(vals,list):
								for val in vals:
										if not super(PropertyListBase,self).checkValue(val):
												return False
								return True
						return False
				def convert(self, vals):
						return [super(PropertyListBase,self).convert(val) for val in vals]
		
				def __repr__(self):
						# val = super(PropertyListBase,self).toString()
						return str(f'{name}({self.getValue()})')

		return PropertyListBase

def PropertyEnumBase(target):
		name = f'{target.__name__}Enum'
		class PropertyEnumBase(target):
				def __init__(self, obj, name, group, description, status, type):
						super().__init__(obj, name, group, description, status, type)
						self.__Values = []
				def checkValue(self,val):
						if isinstance(val,list) and val != self.__Values:
								for v in val:
										if not super(PropertyEnumBase,self).checkValue(v) or (isinstance(v,str) and not v):
												return False
								return True
						elif super(PropertyEnumBase,self).checkValue(val) and len(self.__Values) > 0 and val in self.__Values:
								return True
						else:
								return False
						
				def save(self, reader=None):
						val = super(PropertyEnumBase,self).save(reader)
						val["values"] = self.__Values
						return val
				def getValues(self):
						return self.__Values
				
				def setValue(self, val):
						if isinstance(val,list):
								self.__Values = group_duplicates(val)
								v = super(PropertyEnumBase,self).getValue()
								if v and not v in val:
										super(PropertyEnumBase,self).setValue(None)
						else:
								super(PropertyEnumBase,self).setValue(val)

				def __repr__(self):
						return str(f'{name}({self.toString()})')
				
				def restore(self, reader=None):
						self.setValue(reader['value'])
						self.__Values = reader['values']

		return PropertyEnumBase

class PropertyParameter(PropertyBase):
	def save(self, reader=None):
		data =  super().save(reader)
		data.pop("value")
		return data

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
		
		def add(self, property: type,isList:bool = False, isEnum:bool = False) -> bool:
				name = property.__name__
				if issubclass(property, PropertyBase):
						datas = [
								(name,property)
						]
						if isList:
								datas.append((f'{name}s',PropertyListBase(property)))
						if isEnum:
								datas.append((f'{name}Enum',PropertyEnumBase(property)))
						for item in datas:
								if not item[0] in self.properties:
										self.properties[item[0]] = item[1]
						return True
				return False
		
class HanlderProperty:
		def __init__(self) -> None:
				self.__propertys = []
		@property
		def propertys(self)->list[str]:
			return self.__propertys
		def getProperty(self,name:str):
			property = self.__dict__.get(name)
			return property
		def addProperty(self,type:str,name:str,group:str = '',description:str = '',status:int = 1)->bool:
				mainProperty = MainProperty()
				property = mainProperty.get(type)
				if property:
						name = createAttribute(self,name)
						property = property(self,name,group,description,status,type)
						self.__dict__[name] = property
						self.__propertys.append(name)
						return True
				return None
		
		def checkNameInProperty(self,name:str)->bool:
			return (name in self.__propertys)
		
		def __setattr__(self, name, value):
			if hasattr(self,name) and name in self.__propertys:
				self.__dict__[name].Value = value
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