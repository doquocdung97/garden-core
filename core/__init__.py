from base.document import Document
from .schedule import Schedule, EveryDay, EveryTime
import time,threading,schedule
from common import loggerHelper,check_and_create_folder_log
from base.document import _MainDocument
class Command:
    def Parameter(self):
        """
        return [int,int,str]
        """
        return None
    
    def GetResources(self):
        return {
            "Title","",
            "Tooltip","",
        }

    def IsActive() -> bool:
        return True
    
    def Activated(self,**arg)->any:
        pass
class __MainCommand:
    def __init__(self) -> None:
        self.__commands = {}

    def addCommand(self, name, action):
        if not name in self.__commands:
            self.__commands[name] = action
        else:
            raise ValueError(f"Name: {name} is already in the command")

    def CheckParameter(self,command:Command,*args):
        param = command.Parameter()
        if not param or param and len(param) == len(args):
            for index,arg in enumerate(args):
                if not isinstance(arg,param[index]):
                    return False
        return True
    def runCommand(self, name, *args):
        command = self.getCommand(name)
        if command and command.IsActive():
            if self.CheckParameter(command,*args):
                return command.Activated(*args)
            else:
                raise ValueError("Parameters do not match")
        return None

    def getCommand(self, name: str = None) -> Command | None:
        if name:
            return self.__commands.get(name)
        return self.__commands

class __MainSchedule:
    def __init__(self) -> None:
        self.__schedules = {}

    def add(self, obj:Schedule):
        name = obj.__class__.__name__
        if not name in self.__schedules:
            time = obj.Time()
            if isinstance(time,EveryTime):
                schedule.every(time.minute).minute.do(obj.run)
            self.__schedules[name] = obj
    def remove(self, obj:Schedule):
        #TODO
        name = obj.__class__.__name__
        if name in self.__schedules:
            del self.__schedules[name]
    def loop(self):
        schedule.run_pending()

# cmd = __MainCommand()

class __Core():
    def __init__(self):
        self.__documents = {}
        self.cmd = None
        self.schedule = None
        self.logger = loggerHelper("Core")

        #check and create folder logs
        check_and_create_folder_log()

    def get(self, name: str = None) -> dict| Document | None:
        if not name:
            return self.__documents
        return self.__documents.get(name)

    def create(self, type:str, name:str) -> Document | None:
        main = _MainDocument()
        DocClass = main.get(type)
        if not name in self.__documents and DocClass:
            doc = DocClass()
            doc.setProperties()
            doc.Name = name
            self.__documents[name] = doc

            return self.__documents.get(name)
        return None
    def restore(self,data):
        type = data['type']
        name = data['name']
        main = _MainDocument()
        DocClass = main.get(type)
        if not name in self.__documents and DocClass:
            doc = DocClass()
            doc.restore(data)
            self.__documents[name] = doc

    def loop(self):
        schedule.run_pending()
        # try:
        #     if self.__documents:
        #         for name in self.__documents:
        #             doc = self.get(name)
        #             if doc:
        #                 doc.loop()
        #                 pass
        #     if self.schedule:
        #         self.schedule.loop()
        # except NameError as ex:
        #     self.logger.error(ex)

Core = __Core()
def loop():
    # function to print square of given num
    while True:
        Core.loop()
        time.sleep(1)
loopcore = threading.Thread(target=loop,daemon=True)
loopcore.start()
Core.cmd = __MainCommand()
Core.schedule = __MainSchedule()
import mod
Core.mod = mod.modules