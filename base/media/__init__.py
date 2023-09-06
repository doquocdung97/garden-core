from common import formatName
from common.filehelper import FileHelper
import uuid
from os import path

class Media:
    def __init__(self,doc, pathfile,str_uuid:str = None) -> None:
        self.__pathfile = pathfile
        self.__document = doc
        self.__helper = FileHelper(self.PathFile)
        self.Name = self.__helper.toFileName()
        # self.__type = self.__helper.toFileType()
        self.__data = None
        if not str_uuid:
            self.__uuid = str(uuid.uuid4())
        else:
            self.__uuid = str_uuid
    @property
    def FileName(self):
        return self.__helper.toFileName(True)
    @property
    def UUID(self):
        return self.__uuid
    
    @property
    def Name(self) -> str:
        # if not self.__name:
        #     self.__name = self.__helper.toFileName(self.__pathfile)
        return self.__name
    
    @Name.setter
    def Name(self,val:str) -> str:
        self.__name = formatName(val)

    @property
    def Type(self) -> str:
        # if not self.__type:
        #     self.__type = self.__helper.toFileType(self.__pathfile)
        return self.__helper.toFileType()
    
    @property
    def PathFile(self) -> str:
        return path.join(self.__document.TempDir,self.__pathfile)
    
    @property
    def data(self):
        if not self.__data:
            self.__data = self.__helper.read()
        return self.__data

    def toJSON(self) -> dict:
        return {
            "pathfile": self.__pathfile,
            "uuid":self.__uuid,
            "name":self.Name
        }

    @staticmethod
    def parse(doc, obj: dict):
        filename = obj.get("pathfile")
        str_uuid = obj.get("uuid")
        base = Media(doc,filename,str_uuid)
        base.Name = obj.get("name")
        return base
    
    def onDelete(self):
        return self.__helper.delete()
    
    def __repr__(self):
            # val = super(PropertyListBase,self).toString()
            return str(f'{self.__class__.__name__}({self.__name})')
