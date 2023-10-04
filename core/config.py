import json,os
from constants import VARIATIONS
from appdata import AppDataPaths
from ._version import __project__
class _Config:
  def __init__(self) -> None:
    self.__app_paths = AppDataPaths(__project__)
    self.__data = {}
    self.__pathfile = os.path.join(self.__app_paths.app_data_path,VARIATIONS.CONFIG_FILE_NAME)
    self.__load()
  def __load(self):
    try:
      with open(self.__pathfile, "r") as json_file:
        self.__data = json.load(json_file)
    except:
      pass
  def get(self,name:str,default = None):
    val = self.__data.get(name,default)
    return val
  def set(self,name:str,val):
    self.__data[name] = val
  def delete(self,name:str):
    if self.__data.get(name):
      self.__data.pop(name)
      return True
    return False
  def save(self):
    if not os.path.exists(self.__app_paths.app_data_path):
      os.mkdir(self.__app_paths.app_data_path)
    with open(self.__pathfile, "w") as json_file:
      json.dump(self.__data, json_file, indent=2)
      # json_file.write(json.dumps(self.__data, indent=2).encode("utf-8"))