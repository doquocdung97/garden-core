# from common import formatName
# from common.filehelper import FileHelper
# import uuid
# from os import path
from constants import VARIATIONS
from ..object import MainObject,ObjectBase
from common import createAttribute
from base.model import OBJECTENUM, ObjectModel
class MediaBase(ObjectBase):
	# def tree_view(self, check_in_list=True):
	# 	data = super().tree_view(check_in_list)
	# 	if data:
	# 		data["theme"] = VARIATIONS.MEDIA
	# 	return data
	
	def get_type_object(self):
		return OBJECTENUM.MEDIA

class MainMedia(MainObject):
	pass

class ForderMedia(MediaBase):
	def setProperties(self):
		if not self.checkNameInProperty("Children"):
			self.addProperty("PropertyObjects","Children")
		return super().setProperties()
	def get_command(self):
		return ['CreateFolder','CreateFile']
	
class FileMedia(MediaBase):
	def init(self):
		self.Type = self.__get_type

	def __get_type(self):
		if self.File:
			return self.File.get_type()
		return str()
	
	def setProperties(self):
		if not self.checkNameInProperty("File"):
			self.addProperty("PropertyFile","File")

		if not self.checkNameInProperty("Type"):
			self.addProperty("PropertyStringView","Type")

		return super().setProperties()
	
main = MainMedia()
main.add(ForderMedia)
main.add(FileMedia)
class Media:
	def __init__(self,doc) -> None:
		self.__document = doc
		self.__objects = []
		self.__isChange = False

	def add(self,type,name) ->MediaBase|None:
		main = MainMedia()
		object = main.get(type)
		if object:
			object:MediaBase = object(self)
			object.setProperties()
			name = createAttribute(self,name)
			object.Name = name
			self.__dict__[name] = object
			self.__objects.append(object)
			self.__set_change(True)
			object.init()
			return object
		return None
	
	def __set_change(self,status:bool):
		self.__isChange = status

	def onBeforeChange(self,prop):
		pass
	
	def onChangedObject(self,obj:MediaBase, prop:str):
		self.__set_change(True)
		pass

	def getObjectByName(self,name:str)->MediaBase|None:
		obj = self.__dict__.get(name)
		if isinstance(obj,MediaBase):
			return obj
		
	@property
	def TempDir(self):
		return self.__document.TempDir
	
	def getObjectByUUID(self,uuid:str)->ObjectBase|None:
		for obj in self.Objects:
			if obj.UUID == uuid:
				return obj
		return None
	
	def delete(self,obj:MediaBase):
		if(self.getObjectByName(obj.Name)):
			if obj.onDelete():
				delattr(self,obj.Name)
				self.__objects.remove(obj)
				obj.__del__()
				del obj
				self.__set_change(True)
	
	@property
	def Objects(self)->list[ObjectBase]:  
		return self.__objects
	
	def toJSON(self):
		objects = []
		for object in self.Objects:
			content = object.toJSON()
			objects.append(content)
		return objects
	
	def get_command(self):
		return ["CreateFolder"]
	
	def get_type(self)->str:
			return VARIATIONS.MEDIA
	
	def get_commands(self):
		objs = []
		commands = {}
		commands[self.get_type()] = self.get_command()
		for obj in self.Objects:
			child = obj.tree_view()
			if child:
				objs.append(child)
			obj_type = obj.get_type()
			obj_cmd = obj.get_command()
			if not obj_type in commands and len(obj_cmd) > 0:
				commands[obj_type] = obj_cmd
		return commands
	
	def tree_view(self):
		objs = []
		for obj in self.Objects:
			child = obj.tree_view()
			if child:
				objs.append(child)

		data = {
			'uuid':VARIATIONS.MEDIA,
			'name':VARIATIONS.MEDIA, 
			'type':VARIATIONS.MEDIA, 
			'theme':VARIATIONS.MEDIA,
			'children':objs
		}
		return data
	
	def save(self):
		objects = []
		for object in self.Objects:
			content = object.save()
			objects.append(content)
		return objects
	
	def __restoreObject(self,data):
		type = data['type']
		name = data['name']
		if not hasattr(self,name):
			mainobject = MainObject()
			object = mainobject.get(type)
			if object:
				object:ObjectBase = object(self)
				object.onDocumentRestoredBefore(data)
				# object.restore(data)
				self.__dict__[name] = object
				self.__objects.append(object)
				return (object,data)
	
	def restore(self,render):
		try:
			objs = []
			for object in render:
				data = self.__restoreObject(object)
				objs.append(data)

			for obj,data in objs:
				obj.restore(data)
				obj.init()
				obj.onDocumentRestoredAfter(data)
			self.__set_change(False)
		except Exception as ex:
			# self.__log.error(f"restore document error: {ex}")
			print(f"restore document error: {ex}")

	def deleteObject(self,obj:ObjectBase):
		if(self.getObjectByName(obj.Name)):
			if obj.onDelete():
				delattr(self,obj.Name)
				self.__objects.remove(obj)
				obj.__del__()
				del obj
				self.__set_change(True)
	
	def clone(self):
		main = self.__class__()
		newobjects = []
		for obj in self.__objects:
			newobj = main.addObject(obj.__class__.__name__,obj.Name)
			newobjects.append((obj,newobj))
			obj.setClone(newobj)
		for obj,newobj in newobjects:
			obj._cloneProperty(newobj)
		return main