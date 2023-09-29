
from typing import Any
from base.object import ObjectBase
from base.common import Vector,Color
from .common import *
import os
from common import validate_time
from base.media import Media
main = MainProperty()

class PropertyString(PropertyBase):
		def valueDefault(self):
				return str()
		
		def checkValue(self,val):
				return isinstance(val,str)
main.add(PropertyString,True,True)

class PropertyInteger(PropertyBase):
		def valueDefault(self):
				return 0
		def checkValue(self,val):
				return isinstance(val,int)
main.add(PropertyInteger,True,True)

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
				return isinstance(val,ObjectBase)
		
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
			return self.save()
		
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
from datetime import time

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
			return self.save()
		
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
			return self.save()
		
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
		return self.save()
main.add(PropertyColor,True)