from base.property.common import *
from core import Core,Command,Schedule
from core.schedule import EveryDay, EveryTime
from common import loggerHelper
import datetime
main = MainProperty()
class PropertyJson(PropertyBase):
	def valueDefault(self):
		return {}
	def checkValue(self,vals):
		for val in vals:
			if isinstance(val,dict):
				return False
		return True
main.add(PropertyJson)

class _CommandVector2D(Command):
	def __init__(self) -> None:
		super(_CommandVector2D,self).__init__()
	
	
	def GetResources(self):
		return {
			"Title","Data base",
			"Tooltip","show data",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [int,int,str]
	
	def Activated(self,*args):
		print("ok",args)
		return "dung demo"

Core.cmd.addCommand("Vector2D",_CommandVector2D())