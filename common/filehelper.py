import shutil
from os import path
from .loggerhelper import loggerHelper

__log = loggerHelper("FileHelper")
class FileHelper:
    def __init__(self) -> None:
        # self. __log = loggerHelper(self.__class__.__name__)
        pass
    def upload(self,path:str,file):
        pass
    def copy(self,source_file:str,destination_directory:str):
        shutil.copy(source_file, destination_directory)
    def read(self,path):
        with open(path, 'rb') as binary_file:
            return binary_file.read()
        
    def toFileType(self,file_path:str):
        file_name = path.basename(file_path)
        file_type = path.splitext(file_name)[1]
        return file_type.replace('.',str()) 
    
    def toFileName(self,file_path:str):
        file_name = path.basename(file_path)
        file_type = path.splitext(file_name)[1]
        return file_name.replace(file_type,str())  
