from core import Core,Command
from base.object.common import ObjectBase

class _InsertSeed(Command):
	def GetResources(self):
		return {
			"Title":"Insert Seed",
			"Tooltip":"Insert Seed",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj):
		doc = obj.Document
		
		group = obj.SeedGroup
		if not group:
			group = doc.addObject("ObjectGroup",'Seeds')
			obj.SeedGroup = group
		
		newe_obj = doc.addObject("ObjectSeed",'Seed')
		newe_obj.Indexs = [index for index in range(0,obj.Column*obj.Row)]
		history = group.Children.copy()
		history.append(newe_obj)
		group.Children = history
		return obj.tree_view(False)
Core.cmd.add("InsertSeed",_InsertSeed())

class _StopJob(Command):
	def GetResources(self):
		return {
			"Title":"Stop Job",
			"Tooltip":"Stop Job",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj):

		if hasattr(obj,"Grbl"):
			obj.Grbl.remove_job()
	
Core.cmd.add("StopJob",_StopJob())

class _GoHome(Command):
	def GetResources(self):
		return {
			"Title":"Go Home",
			"Tooltip":"Go Home",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj):

		if hasattr(obj,"Grbl"):
			obj.Grbl.GoHome()
	
Core.cmd.add("GoHome",_GoHome())

class _UpdatePoint(Command):
	def GetResources(self):
		return {
			"Title":"Update Point",
			"Tooltip":"Update Point",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj):

		if hasattr(obj,"HandlePoints"):
			obj.HandlePoints()
	
Core.cmd.add("UpdatePoint",_UpdatePoint())

class _ReConnect(Command):
	def GetResources(self):
		return {
			"Title":"Re Connect",
			"Tooltip":"Re Connect",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj):

		if hasattr(obj,"connect"):
			obj.connect()
	
Core.cmd.add("ReConnect",_ReConnect())

class _GetSetingByGrbl(Command):
	def GetResources(self):
		return {
			"Title":"Get Seting By Grbl",
			"Tooltip":"Get Seting By Grbl",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj):

		if hasattr(obj,"GetSetingByGrbl"):
			obj.GetSetingByGrbl()
	
Core.cmd.add("GetSetingByGrbl",_GetSetingByGrbl())

class _SetSetingForGrbl(Command):
	def GetResources(self):
		return {
			"Title":"Set Seting For Grbl",
			"Tooltip":"Set Seting For Grbl",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj):

		if hasattr(obj,"SetSetingForGrbl"):
			obj.SetSetingForGrbl()
	
Core.cmd.add("SetSetingForGrbl",_SetSetingForGrbl())