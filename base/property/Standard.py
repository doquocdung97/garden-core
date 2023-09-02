
from typing import Any
from base.object import ObjectBase
from base.common import Vector
from .common import *
import os
from common import validate_time
main = MainProperty()

class PropertyString(PropertyBase):
    def valueDefault(self):
        return str()
    
    def checkValue(self,val):
        if isinstance(val,str):
            return True
        else:
            return False
main.add(PropertyString,True,True)

class PropertyInteger(PropertyBase):
    def valueDefault(self):
        return 0
    def checkValue(self,val):
        if isinstance(val,int):
            return True
        else:
            return False
main.add(PropertyInteger,True,True)

class PropertyBool(PropertyBase):
    def valueDefault(self):
        return False
    
    def checkValue(self,val):
        if isinstance(val,bool):
            return True
        else:
            return False
main.add(PropertyBool,True)

class PropertyFloat(PropertyBase):
    def valueDefault(self):
        return 0.0
    def checkValue(self,val):
        if isinstance(val,float):
            return True
        else:
            return False
main.add(PropertyFloat,True,True)

class PropertyFile(PropertyBase):
    def valueDefault(self):
        return str()
    def getValue(self,isSave = False):
        filename =  self.__Value
        if self.__Value:
            filename = os.path.join(self.object.Document.TempDir,self.__Value)
            if not os.path.exists(filename):
                filename = ''
        return filename
        
    def checkValue(self,val):
        if isinstance(val,str) and os.path.exists(val):
            return True
        else:
            raise ValueError('not file')
            return False
    def setValue(self,val):
        from shutil import copyfile
        filename = os.path.join(self.object.Document.TempDir,os.path.basename(val))

        copyfile(val, filename)

        self.__Value = os.path.basename(val)

    def save(self,reader):
        if self.getValue() not in reader['file']:
            reader['file'].append(self.getValue())

        return super(PropertyFile,self).save(reader)
    def restore(self,reader = None):
        self.__Value = reader['value']
        pass
    def toString(self):
        return self.__Value
main.add(PropertyFile)

class PropertyObject(PropertyBase):
    
    def checkValue(self,val:ObjectBase)->bool:
        if isinstance(val,ObjectBase):
            return True
        else:
            return False
    
    def getValue(self, isSave=False):
        value = super(PropertyObject,self).getValue(isSave)
        
        if isSave and value:
            if isinstance(value,list):
                    return [v.UUID for v in value]
            return value.UUID
        return value
    
    def setValue(self, val):
        super(PropertyObject,self).setValue(val)


    def convert(self,val):
        doc = self.object.Document
        return doc.getObjectByUUID(val)

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
    
main.add(PropertyVector,True)