from base.document import Document
from .schedule import Schedule, EveryDay, EveryTime
import schedule
import threading
import time

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
    def CheckParameter(self,*args):
        param = self.Parameter()
        if param and len(param) == len(args):
            for index,arg in enumerate(args):
                if not isinstance(arg,param[index]):
                    return False
            return True
        return False
    def Activated(self,**arg)->any:
        pass
class __MainCommand:
    def __init__(self) -> None:
        self.__commands = {}

    def addCommand(self, name, action):
        if not name in self.__commands:
            self.__commands[name] = action

    def runCommand(self, name, *args):
        command = self.__commands.get(name)
        if (command and command.IsActive() and command.CheckParameter(*args)):
            return command.Activated(*args)
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

    def get(self, name: str = None) -> list[Document] | Document | None:
        if not name:
            return self.__documents
        return self.__documents.get(name)

    def create(self, name) -> Document | None:
        if not name in self.__documents:
            self.__documents[name] = Document()
            return self.__documents.get(name)
        return None
    def loop(self):
        if self.schedule:
            self.schedule.loop()

Core = __Core()
def loop():
    # function to print square of given num
    while True:
        Core.loop()
        time.sleep(100)
loopcore = threading.Thread(target=loop,daemon=True)
loopcore.start()
Core.cmd = __MainCommand()
Core.schedule = __MainSchedule()
import mod
Core.mod = mod.modules