from base.property import HanlderProperty, PropertyBase

class PropertyParameter:
	def __init__(self,property:PropertyBase) -> None:
		self.__property = property
		self.__inlist = []
		
	def getValue(self,isSave = False):
		return self.__property.getValue(isSave)
	
	def setValue(self,val):
		self.__property.Value = val

	def toJSON(self):
		return self.__property.toJSON()
	
	def getType(self):
		return self.__property.getType()
	
	def toString(self):
		return f"Parameter.{self.__property.getName()}"
	
	def onChange(self):
		for pro in self.__inlist:
			pro.onChange()
	def addInList(self,obj:PropertyBase):
		self.__inlist.append(obj)
class Parameter(HanlderProperty):
	def __init__(self) -> None:
		super().__init__()
		self.__parameterpropertys = {}

	def addProperty(self, type: str, name: str, group: str = '', description: str = '', status: int = 1, attribute=None) -> PropertyBase | None:
		pro = super().addProperty(type, name, group, description, status, attribute)
		self.__parameterpropertys[pro.getName()] = PropertyParameter(pro)
	
	def save(self):
		return self.saveProperty()

	def toJSON(self):
		return self.toJSONProperty()

	def __getattribute__(self, name):
			try:
				property =  super(HanlderProperty,self).__getattribute__(name)
				if isinstance(property,PropertyBase):
					return self.__get(name)
			except:
				pass
			return super(HanlderProperty,self).__getattribute__(name)
	def __get(self,name)->PropertyParameter|None:
		return self.__parameterpropertys.get(name)
	def onBeforeChange(self, prop):
		return super().onBeforeChange(prop)
	
	def onChanged(self, prop):
		super().onChanged(prop)
		param = self.__get(prop)
		if param:
			param.onChange()