from ..property import HanlderProperty
import uuid
from common import loggerHelper,createAttribute
class ObjectBase(HanlderProperty):
	
	def __init__(self,document):
		super(ObjectBase,self).__init__()
		self.__document = document
		self.__isChange = False
		self.UUID = str(uuid.uuid4())
		self.Name = str()

	def setProperties(self):
		if not "Label" in self.propertys:
			self.addProperty('PropertyString','Label')

	def save(self,reader):
		propertys = []
		for property in self.propertys:
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
			if property['name'] in self.propertys:
				self.__dict__[property['name']].restore(property)
	
	def IsChange(self):
		return self.__isChange
	def setChange(self,status):
		self.__isChange = status
	@property
	def Document(self):
		return self.__document

	def onDocumentRestoredBefore(self,reader):
		self.UUID = reader['uuid']
		self.Name = reader['name']
		pass
	def onDocumentRestoredAfter(self,reader:dict):
		pass

	def execute(self):
		self.__document.setChange(True)
		self.setChange(False)

	def init(self):
		self.logger = loggerHelper(f"Object({self.Name})")

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