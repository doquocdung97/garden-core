from ..property import common
import uuid
from common import loggerHelper,createAttribute
class ObjectBase:
	def __init__(self,document):
		self.__document = document
		self.__isChange = False
		self.__propertys = []
		self.UUID = str(uuid.uuid4())
		self.Name = str()
	def setProperties(self):
		if not "Label" in self.__propertys:
			self.addProperty('PropertyString','Label')

	def save(self,reader):
		propertys = []
		for property in self.__propertys:
			dataproperty = self.__dict__[property].save(reader)
			propertys.append(dataproperty)

		return {
			'uuid':self.UUID,
			'type':self.__class__.__name__,
			'name':self.Name, 
			'propertys':propertys
		}
		
	def restore(self,reader):
		for property in reader["propertys"]:
			self.addProperty(property['type'],property['name'],property['group'],property['tip'],property['status'])
			if property['name'] in self.__propertys:
				self.__dict__[property['name']].restore(property)
	
	def IsChange(self):
		return self.__isChange
	def setChange(self,status):
		self.__isChange = status
	@property
	def Document(self):
		return self.__document
	@property
	def propertys(self):
		return self.__propertys

	def onDocumentRestoredBefore(self,reader):
		self.UUID = reader['uuid']
		self.Name = reader['name']
		pass
	def onDocumentRestoredAfter(self,reader:dict):
		pass
	def addProperty(self,type:str,name:str,group:str = '',tip:str = '',status:int = 1)->bool:
		mainProperty = common.MainProperty()
		property = mainProperty.get(type)
		if property:
			name = createAttribute(self,name)
			property = property(self,name,group,tip,status,type)
			self.__dict__[name] = property
			self.__propertys.append(name)
			return True
		return None
	
	def __setattr__(self, name, value):
		if hasattr(self,name) and name in self.__propertys:
			self.__dict__[name].Value = value
			return
		return super().__setattr__(name, value)

	def __getattribute__(self, name):
		try:
			property =  super().__getattribute__(name)
			if isinstance(property,common.PropertyBase):
				return property.Value
		except:
			pass
		return super().__getattribute__(name)

	def execute(self):
		self.__document.setChange(True)
		self.setChange(False)

	def init(self):
		self.logger = loggerHelper(f"Object({self.Name})")
	def getProperty(self,name:str):
		property = self.__dict__.get(name)
		return property
	def onBeforeChange(self,prop):
		pass
	def onDelete(self)->bool:
		return True
	def onChanged(self, prop):
		pass
	def __repr__(self):
		return self.__class__.__name__ + "({0})".format(self.Name)
class MainObject():
	__properties = {}
	def get(self,name:str =None)->type|None:
		if not name:
			return self.__properties
		return self.__properties.get(name)

	def add(self,name,property)->bool:
		if not name in self.__properties:
			self.__properties[name] = property
			return True
		return False
	
main = MainObject()
main.add(ObjectBase.__name__,ObjectBase)