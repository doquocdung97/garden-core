from enum import Enum, auto
from common import loggerHelper
class DayType(Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    EVERYDAY = 7
    
class EveryDay:
    def __init__(self,hour:int,minute:int,day:DayType) -> None:
        self.day = day
        self.hour = hour
        self.minute = minute

class EveryTime:
    def __init__(self,minute:int) -> None:
        self.minute = minute

class Schedule:
    
    def __init__(self) -> None:
        self.logger = loggerHelper(self.__class__.__name__)
        pass
    def Time(self)->EveryDay|EveryTime:
        pass
    def IsActive(self) -> bool:
        return True
    def run(self):
        try:
            if self.IsActive():
                self.Activated()
        except NameError as ex:
            self.logger.error(ex)
    
    def Activated(self):
        pass

