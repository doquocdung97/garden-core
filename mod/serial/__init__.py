from core import Core,Command,Schedule
from serial.tools import list_ports
class _ListSerial(Command):
	def GetResources(self):
		return {
			"Title","Serials",
		}

	def IsActive(self) -> bool:
		return True
	
	# def Parameter(self):
	#     return [int,int,str]
	
	def Activated(self,*args):
		return list_ports.comports()

Core.cmd.addCommand("ListSerial",_ListSerial())