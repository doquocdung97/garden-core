from base.document import Document
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
    def Activated(self,**arg):
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
            command.Activated(*args)

    def getCommand(self, name: str = None) -> Command | None:
        if name:
            return self.__commands.get(name)
        return self.__commands

# cmd = __MainCommand()
class __Core():
    def __init__(self):
        self.__documents = {}
        self.__cmd = None
        
    @property
    def cmd(self):
        return self.__cmd

    @cmd.setter
    def cmd(self, val):
        self.__cmd = val

    def get(self, name: str = None) -> list[Document] | Document | None:
        if not name:
            return self.__documents
        return self.__documents.get(name)

    def create(self, name) -> Document | None:
        if not name in self.__documents:
            self.__documents[name] = Document()
            return self.__documents.get(name)
        return None
Core = __Core()
Core.cmd = __MainCommand()
import mod
Core.mod = mod.modules