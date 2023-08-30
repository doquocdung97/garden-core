
from base.object import ObjectBase
from .common import *
import os
main = MainProperty()

class PropertyString(PropertyBase):
    def valueDefault(self):
        return str()
    
    def checkValue(self,val):
        if isinstance(val,str):
            return True
        else:
            return False
main.addHasList(PropertyString)

class PropertyInteger(PropertyBase):
    def valueDefault(self):
        return 0
    def checkValue(self,val):
        if isinstance(val,int):
            return True
        else:
            return False
main.addHasList(PropertyInteger)

class PropertyBool(PropertyBase):
    def valueDefault(self):
        return False
    
    def checkValue(self,val):
        if isinstance(val,bool):
            return True
        else:
            return False
main.addHasList(PropertyBool)

class PropertyFloat(PropertyBase):
    def valueDefault(self):
        return 0.0
    def checkValue(self,val):
        if isinstance(val,float):
            return True
        else:
            return False
main.addHasList(PropertyFloat)

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
        self.__Value = reader.dataRestore['value']
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
            return value.UUID
        return value
    
    def setValue(self, val):
        super(PropertyObject,self).setValue(val)

    def toString(self):
        return self.__Value
main.add(PropertyObject)