from base.property.common import *
from core import Core,Command,Schedule
from core.schedule import EveryDay, EveryTime
from common import loggerHelper
import datetime
main = MainProperty()

class _WaterFlow(Command):
	def GetResources(self):
		return {
			"Title","Water flow",
			"Tooltip","Water flow",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [int,int,str]
	
	def Activated(self,*args):
		print("ok dung demo _WaterFlow",args)
		return "dung demo _WaterFlow"

class _Temperature(Command):
	def GetResources(self):
		return {
			"Title","Temperature",
		}

	def IsActive(self) -> bool:
		return True
	
	# def Parameter(self):
	#     return [int,int,str]
	
	def Activated(self,*args):
		print("ok dung demo Temperature",args)
		return "dung demo Temperature"


Core.cmd.add("WaterFlow",_WaterFlow())
Core.cmd.add("Temperature",_Temperature())