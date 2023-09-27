from common import group_duplicates,createAttribute
from  inspect import ismethod,isfunction

class PropertyBase:
		def __init__(self, obj, name, group, description, status, type,attribute):
				self.object = obj
				self.__Name = name
				self.__type = type
				self.group = group
				self.description = description
				self.status = status
				self.attribute = attribute
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
								from base.object import ObjectBase
								if isinstance(self.object,ObjectBase):
									self.object.Document.onChangedObject(self.object,self.__Name)
								# self.object.setChange(True)
				else:
						raise ValueError('not value type')

		def getType(self):
				return self.__class__.__name__

		def save(self):
				return {
						'name': self.__Name,
						'type': self.__type,
						'value': self.getValue(True),
						'group': self.group,
						'description': self.description,
						'status': self.status,
						'attribute':self.attribute
				}
		
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
		def clone(self):
			pro = self.__class__(self.object,self.__Name,self.group,self.description,self.status,self.__type,self.attribute)
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
				def __init__(self, obj, name, group, description, status, type, attribute):
						super().__init__(obj, name, group, description, status, type, attribute)
						self.__Values = []
				def checkValue(self,val):
						if ismethod(val) and self.object.__getattribute__(val.__func__.__name__) :
							return True
						elif isinstance(val,list) and val != self.getValues():
								for v in val:
										if not super(PropertyEnumBase,self).checkValue(v) or (isinstance(v,str) and not v):
												return False
								return True
						elif super(PropertyEnumBase,self).checkValue(val) and len(self.getValues()) > 0 and val in self.getValues():
								return True
						else:
								return False
						
				def save(self):
						data = super(PropertyEnumBase,self).save()
						val = self.__Values
						data["values"] = val
						return data
				
				def toJSON(self):
					data = super(PropertyEnumBase,self).save()
					data["values"] = self.getValues()
					return data
				
				def getValues(self):
						if isinstance(self.__Values,str):
							return self.object.__getattribute__(self.__Values)(self)
						return self.__Values
				
				def setValue(self, val):
						if ismethod(val) or isfunction(val):
							self.__Values = val.__func__.__name__
							super(PropertyEnumBase,self).setValue(None)
						elif isinstance(val,list):
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

				def clone(self):
					pro = super(PropertyEnumBase,self).clone()
					pro.__Values = self.__Values
					pro.Value = self.Value
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
			if ismethod(val) or isfunction(val):
				super(PropertyViewBase,self).setValue(val)
			else:
				raise ValueError('value only read')
		
		def save(self):
			return super(PropertyViewBase,self).save()
		
		def getValue(self, isSave=False):
			val = super(PropertyViewBase,self).getValue()
			if ismethod(val) or isfunction(val):
				return val()
			return self.valueDefault()
		
		def __repr__(self):
			return str(f'{name}({self.toString()})')
		
	return PropertyViewBase

def PropertyParameterBase(target):
	name = f'{target.__name__}Parameter'
	class PropertyParameterBase(target):
		def save(self):
			data =  super().save()
			data.pop("value")
			return data
		def __repr__(self):
			return str(f'{name}({self.toString()})')
		
	return PropertyParameterBase

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
		
		def add(self, property: type,isList:bool = False, isEnum:bool = False, isView:bool = False, isParameter:bool = False) -> bool:
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
						if isParameter:
							datas.append((f'{name}Parameter',PropertyParameterBase(property)))
						for item in datas:
								if not item[0] in self.properties:
										self.properties[item[0]] = item[1]
						return True
				return False
		
class HanlderProperty:
		def __init__(self) -> None:
				self.__propertys = []
		
		def isInit(self):
			return True
		
		@property
		def propertys(self)->list[str]:
			return self.__propertys
		
		def getProperty(self,name:str)->PropertyBase|None:
			if name in self.__propertys:
				property = self.__dict__.get(name)
				return property
		
		def addProperty(self,type:str,name:str,group:str = '',description:str = '',status:int = 1,attribute = None)->PropertyBase|None:
				mainProperty = MainProperty()
				property = mainProperty.get(type)
				if property:
						name = createAttribute(self,name)
						property = property(self,name,group,description,status,type,attribute)
						self.__dict__[name] = property
						self.__propertys.append(name)
						return property
				return None
		
		def restoreProperty(self,reader):
			for property in reader:
				self.addProperty(property['type'],property['name'],property['group'],property['description'],property['status'],property['attribute'])
				if property['name'] in self.propertys:
					self.__dict__[property['name']].restore(property)
					
		
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
		
		def _cloneProperty(self,target):
			for name in self.__propertys:
				pro = self.__dict__[name]
				pro = pro.clone()
				target.__dict__[name] = pro
				if not name in target.__propertys:
					target.__propertys.append(name)