from common.filehelper import FileHelper
import uuid
from os import path

class Media:
    def __init__(self,doc, pathfile) -> None:
        self.__helper = FileHelper()
        self.__pathfile = pathfile
        self.__document = doc
        self.__name = self.__helper.toFileName(self.__pathfile)
        self.__type = self.__helper.toFileType(self.__pathfile)
        self.__data = None
        self.__uuid = str(uuid.uuid4())
        pass
    
    @property
    def UUID(self):
        return self.__uuid
    @property
    def Name(self) -> str:
        # if not self.__name:
        #     self.__name = self.__helper.toFileName(self.__pathfile)
        return self.__name

    @property
    def Type(self) -> str:
        # if not self.__type:
        #     self.__type = self.__helper.toFileType(self.__pathfile)
        return self.__type
    
    @property
    def PathFile(self) -> str:
        return path.join(self.__document.TempDir,self.__pathfile)
    
    @property
    def data(self):
        if not self.__data:
            self.__data = self.__helper.read(self.PathFile)
        return self.__data

    def toJSON(self) -> dict:
        return {
            "pathfile": self.__pathfile,
            "uuid":self.__uuid
        }

    @staticmethod
    def parse(doc, obj: dict):
        filename = obj.get("pathfile")
        filename = obj.get("uuid")

    def onDelete(self):
        pass
