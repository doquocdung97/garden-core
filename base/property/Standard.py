

from common import *
import os
main = MainProperty()
class PropertyString(PropertyBase):
    def __init__(self,obj,name,group,tip,status):
        super(PropertyString,self).__init__(obj,name,group,tip,status)
        self.__Value = ''
    def getValue(self,isSave = False):
        return self.__Value
    def checkValue(self,val):
        if isinstance(val,str):
            return True
        else:
            return False
    def setValue(self,val):
        self.__Value = val

    def getType(self):
        return self.__class__.__name__
    def toString(self):
        return self.__Value
main.add(PropertyString)

class PropertyInteger(PropertyBase):
    def __init__(self,obj,name,group,tip,status):
        super(PropertyInteger,self).__init__(obj,name,group,tip,status)
        self.__Value = 0
    def getValue(self,isSave = False):
        return self.__Value
    def checkValue(self,val):
        if isinstance(val,int):
            return True
        else:
            return False
    def setValue(self,val):
        self.__Value = val
    def getType(self):
        return self.__class__.__name__
    def toString(self):
        return self.__Value
main.add(PropertyInteger)

class PropertyBool(PropertyBase):
    def __init__(self,obj,name,group,tip,status):
        super(PropertyBool,self).__init__(obj,name,group,tip,status)
        self.__Value = False
    def getValue(self,isSave = False):
        return self.__Value
    def checkValue(self,val):
        if isinstance(val,bool):
            return True
        else:
            return False
    def setValue(self,val):
        self.__Value = val

    def toString(self):
        return self.__Value
      
main.add(PropertyBool)

class PropertyFile(PropertyBase):
    def __init__(self,obj,name,group,tip,status):
        super(PropertyFile,self).__init__(obj,name,group,tip,status)
        self.__Value = ''
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


class PropertyLink(PropertyBase):
    def __init__(self,obj,name,group,tip,status):
        super(PropertyLink,self).__init__(obj,name,group,tip,status)
        self.__Value = None
    def getValue(self,isSave = False):
        return self.__Value
    def checkValue(self,val):
        if isinstance(val,bool):
            return True
        else:
            return False
    def setValue(self,val):
        self.__Value = val

    def toString(self):
        return self.__Value
      
main.add(PropertyLink)
