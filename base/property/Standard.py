
from typing import Any
from base.object import ObjectBase
from base.common import Vector,Color,File,FileObject
from .common import *
import os
from common import validate_time
from base.media import Media
from datetime import time
main = MainProperty()

class PropertyString(PropertyBase):
		def valueDefault(self):
				return str()
		
		def checkValue(self,val):
				return isinstance(val,str)
main.add(PropertyString,True,True,True)

class PropertyInteger(PropertyBase):
		def valueDefault(self):
				return 0
		def checkValue(self,val):
				return isinstance(val,int)
		def convert(self, val):
			return int(val)
main.add(PropertyInteger,True,True,True)

class PropertyBool(PropertyBase):
		def valueDefault(self):
				return False
		
		def checkValue(self,val):
				return isinstance(val,bool)
main.add(PropertyBool,True,isView=True)

class PropertyFloat(PropertyBase):
		def valueDefault(self):
				return 0.0
		def checkValue(self,val):
				return isinstance(val,float) or isinstance(val,int)
		def setValue(self, val):
			if isinstance(val,int):
				val = float(val)
			return super().setValue(val)
		def convert(self, val):
			return float(val)
main.add(PropertyFloat,True,True)

class PropertyMedia(PropertyBase):
		def getValue(self, isSave=False):
				value = super(PropertyMedia,self).getValue(isSave)
				if isSave and value:
						if isinstance(value,list):
										return [v.UUID for v in value]
						return value.UUID
				return value
				
		def checkValue(self,val):
				return isinstance(val,Media)
		
		def toJSON(self):
			data = super(PropertyMedia,self).toJSON()
			val = super(PropertyMedia,self).getValue()
			if val:
				if isinstance(val,list):
					data["value"] = [v.toJSON() for v in val]
				else:
					data["value"] = val.toJSON()
			
			return data
			
		def convert(self, val):
				doc = self.object.Document
				return doc.getMediaByUUID(val)

		def toString(self):
				return self.__Value
		
		def clone(self):
			pro = super().clone()
			if isinstance(pro.Value,list):
				pro.Value = [v.Clone for v in pro.Value]
			else:
				pro.Value = pro.Value.Clone
			return pro
		
main.add(PropertyMedia,True)

class PropertyObject(PropertyBase):
		def checkValue(self,val:ObjectBase)->bool:
				return isinstance(val,ObjectBase) or val is None
		
		def getValue(self, isSave=False):
				value = super(PropertyObject,self).getValue(isSave)
				
				if isSave and value:
						if isinstance(value,list):
										return [v.UUID for v in value]
						return value.UUID
				return value
		
		def setValue(self, val):
				super(PropertyObject,self).setValue(val)

		def toJSON(self):
			data = self.save()
			val = self.getValue()
			
			if isinstance(val,list):
				data['value'] = [{"name":v.Name,"uuid":v.UUID}  for v in val]
			elif val:
				data['value'] = {
					"name":val.Name,
					"uuid":val.UUID
				} 
			return data
		
		def convert(self,val):
				doc = self.object.Document
				return doc.getObjectByUUID(val)
		
		def clone(self):
			pro = super().clone()
			if isinstance(pro.Value,list):
				pro.Value = [v.Clone for v in pro.Value]
			else:
				pro.Value = pro.Value.Clone
			return pro

main.add(PropertyObject,True)

class PropertyTime(PropertyBase):
		def valueDefault(self):
				return time(0,0)
		
		def checkValue(self,val:time):
				return isinstance(val,time)
		def convert(self,val):
				return time(val.get("hour"),val.get("minute"),val.get("second"))

		def getValue(self, isSave=False):
				if isSave:
						val:time = self.getValue()
						return {
								"hour":val.hour,
								"minute":val.minute,
								"second":val.second,
						}
				return super().getValue(isSave)
		def toJSON(self):
			data = super().toJSON()
			data["value"] = self.getValue(True)
			return data
		
main.add(PropertyTime)

class PropertyVector(PropertyBase):
		def valueDefault(self):
				return Vector()
		
		def checkValue(self,val:Vector):
				return isinstance(val,Vector)
		
		def convert(self, val):
				return Vector.parse(val)

		def getValue(self, isSave=False):
				if isSave:
						val:Vector = super().getValue()
						if val:
								if isinstance(val,list):
										return [v.toJSON() for v in val]
								return val.toJSON()
				return super().getValue(isSave)
		def toJSON(self):
			data = super().toJSON()
			data["value"] = self.getValue(True)
			return data
		
main.add(PropertyVector,True)

class PropertyColor(PropertyBase):
	def valueDefault(self):
		return Color()
	
	def checkValue(self,val:Color):
		return isinstance(val,Color)
	
	def convert(self, val):
		return Color.parse(val)

	def getValue(self, isSave=False):
		if isSave:
			val:Color = super().getValue()
			if val:
				if isinstance(val,list):
					return [v.toJSON() for v in val]
				return val.toJSON()
		return super().getValue(isSave)
	def toJSON(self):
		data = super().toJSON()
		data["value"] = self.getValue(True)
		return data
main.add(PropertyColor,True)

class PropertyDocument(PropertyBase):
	
	def checkValue(self,val:any):
		from base.document import Document
		return isinstance(val,Document)
	
	def convert(self, val):
		from core import Core

		doc = Core.openTemplate(val)
		return doc

	def getValue(self, isSave=False):
		val = super().getValue(isSave)
		if isSave and val:
			return val.FileName
		return val
	
	def setValue(self, val):
		return super().setValue(val)
	
	def toJSON(self):
		data = super().toJSON()
		val = super().getValue()
		if val:
			data["value"] = val.toJSON()
		return data
	
main.add(PropertyDocument)

class PropertyFunction(PropertyBase):
	def __init__(self, obj, name, group, description, status, type, attribute):
		super().__init__(obj, name, group, description, status, type, attribute)
		self.__func = None
	def checkValue(self, val):
		return ismethod(val) or isfunction(val)
	
	def setValue(self, val):
		self.__func = val

	def toJSON(self):
		data = super().toJSON()
		del data["value"]
		return data

	def save(self):
		data = super().save()
		del data['value']
		return data

	def getValue(self, isSave=False):
		return self.__func
main.add(PropertyFunction)

class PropertyFile(PropertyBase):
	def valueDefault(self):
		return None
	
	def checkValue(self,val:File):
		return isinstance(val,File) or isinstance(val,FileObject) or val == None
	
	def convert(self, val):
		obj = self.object
		if not isinstance(val,str):
			path = os.path.join(obj.UUID,val.name)
			f = open(os.path.join(obj.Document.TempDir,path), "wb")
			f.write(val.read())
			f.close()
			val = path
		return FileObject.parse(obj,val)

	def getValue(self, isSave=False):
		if isSave:
			val:FileObject = super().getValue()
			if val:
				if isinstance(val,list):
					return [v.save() for v in val]
				return val.save()
		return super().getValue(isSave)

	def toJSON(self):
		jsondata = super().toJSON()
		val:FileObject = super().getValue()
		data = None
		if val:
				if isinstance(val,list):
					data = [v.toJSON() for v in val]
				data = val.toJSON()
		jsondata["value"] = data
		return jsondata
	
	def setValue(self, val:File):
		old_val = self.getValue()
		if isinstance(old_val,FileObject):
			old_val.delete()
		if val and isinstance(val,File):
			val = FileObject(self.object,val)
		return super().setValue(val)

		
main.add(PropertyFile)