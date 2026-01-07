from base.property import HanlderProperty, PropertyBase
from constants.variables import VARIATIONS

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

	def onDelete(self):
		for pro in self.__inlist:
			pro.Value = pro.Value
		self.__inlist = []
		
class Parameter(HanlderProperty):
	def __init__(self,doc) -> None:
		super().__init__()
		self.__document = doc
		self.__parameterpropertys = {}

	@property
	def Document(self):
		return self.__document
	
	@property
	def Model(self):
		return self.__document.Model
	
	def addProperty(self, type: str, name: str, group: str = '', description: str = '', status: int = 1, attribute={},model = False) -> PropertyBase | None:
		attribute[VARIATIONS.PARAMETER] = True
		pro = super().addProperty(type, name, group, description, status, attribute,model)
		self.__parameterpropertys[pro.getName()] = PropertyParameter(pro)
		self.__document.onCreateParameter(pro)
		return pro
	
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
		self.__document.onChangedParameter(prop)
		param = self.__get(prop)
		if param:
			param.onChange()
	
	def deleteProperty(self,prop):
		param = self.__get(prop)
		if param:
			param.onDelete()
			del self.__parameterpropertys[prop]

		super().deleteProperty(prop)