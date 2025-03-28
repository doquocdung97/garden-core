import time, schedule
from serial.tools import list_ports
import asyncio
from base.object.common import MainObject, ObjectBase
from mod.serial import ObjectSerial
import threading

class ObjectGrbl(ObjectSerial):
	def setProperties(self):
		result = super().setProperties()
		if not self.checkNameInProperty("Job"):
			self.addProperty("PropertyBool","Job")
			self.Job = True

		if not self.checkNameInProperty("Setting"):
			self.addProperty("PropertyJson","Setting")
			self.Setting = {}

		return result
	
	def init(self):
		self.msg = ""
		self.Status = None
		self.__job = None
		self.__list_job = []
		return super().init()
	
	def listport(self,property):
		return [v.device for v in list_ports.comports()]
	
	def PlusPosition(self,status = True):
		if status:
			return self.send("G91\n")
		else:
			return self.send("G90\n")

	def SetPosition(self,x = None,y = None,z = None,speed = None,isIdle = True):
		code = "G0"
		str_speed = str()
		if speed:
			code = "G01"
			str_speed = "F{}".format(speed)
		str_x = str()
		if not x is None:
			str_x = "X{}".format(x)

		str_y = str()
		if not y is None:
			str_y = "Y{}".format(y)
		
		str_z = str()
		if not z is None:
			str_z = "Z{}".format(z)
		# 	return self.send("G01 X{} Y{} Z{} F{}\n".format(x,y,z,speed),False,True)
		# return self.send("G0 X{} Y{} Z{}\n".format(x,y,z),False,True)
		self.append_job("{} {} {} {} {}\n".format(code,str_x,str_y,str_z,str_speed),isIdle=isIdle)

	def SetSpeed(self,speed):
		return self.send("F{}\n".format(speed))

	def GoHome(self,job = False):
		
		if job:
			self.append_job("$X",isIdle=False)
			self.append_job("G92 X-500 Y-500 Z-500",isIdle=True)
			self.append_job("$H",isIdle=True)
			self.append_job("G92 X0 Y0 Z0",isIdle=True)
		else:
			self.send("$X\n")
			self.send("G92 X-500 Y-500 Z-100")
			self.send("$H")
			self.send("G92 X0 Y0 Z0",False,True)

	def connect(self):
		ser =  super().connect()
		self.__setJob()
		return ser
	
	def sendAsync(self,val:str):
		if self.IsOpen:
			try:
				mess = bytes(f"{val}\r\n", 'utf-8')
				self.ser.write(mess)
				time.sleep(0.1)
				response = []
				count = 1000
				while count > 0:
					line = self.ser.readline().decode().strip()
					if line:
						response.append(line)
					time.sleep(0.1)
					if "ok" in line.lower() or "error" in line.lower():  # Stop on complete response
								break
					count -=1
				print(response)
				return response
			except Exception as ex:
				self.logger.error(ex)
		return
	
	def send(self,val:str,result = False,isIdle = False):
		if self.IsOpen:
			try:
				count = 100
				while count > 0 and isIdle: 
					if self.Status and self.Status.get("status") == "Idle":
						break
					time.sleep(0.1)
					count -=1
				mess = bytes(f"{val}\r\n", 'utf-8')
				self.ser.write(mess)
				if result:
					return self.read()
			except Exception as ex:
				self.logger.error(ex)
	
	def append_job(self,cmd,isIdle = True,time = 0):
		self.__list_job.append({"cmd":cmd,"isIdle":isIdle,"time":time})

	def remove_job(self, index = None):
		if index is None:
			self.__list_job = []
		elif 0 <= index < len(self.__list_job):
			del self.__list_job[index]

	def __setJob(self):
		try:
			if self.__job:
				schedule.cancel_job(self.__job)
			if self.IsOpen and hasattr(self,"Job") and self.Job:
				self.__job = schedule.every(self.Timeout).seconds.do(self.__schedule_task)
		except Exception as ex:
			print(ex)

	def __schedule_task(self):
		"""
		Schedules a task to run at a specified interval in milliseconds.

		:param callback: The function to execute.
		:param interval_ms: Time interval in milliseconds.
		"""
		try:
			if len(self.__list_job) > 0:
				self.Status = self.__handle_status()
				index = 0
				job = self.__list_job[index]
				cmd = job.get("cmd")
				if job and cmd:
					if (job.get("isIdle") == True and self.Status and self.Status.get("status") == "Idle") or (not job.get("isIdle") and self.Status):
						self.send(cmd)
						self.remove_job(index)
						print(cmd)
		except Exception as ex:
			print(ex)

	def __handle_status(self):
		if self.IsOpen:
			msgs = self.send("?",True)
			result = None
			if msgs and len(msgs) > 0:
				if msgs.startswith('<') and '|' in msgs:
					parts = msgs[1:-1].split('|')  # Remove '<' and '>'
					status = parts[0]  # Machine status (Idle, Run, Hold, etc.)
					position = {}
					# Find position data (MPos or WPos)
					for part in parts:
							if part.startswith("MPos:") or part.startswith("WPos:"):
									coords = part.split(':')[1].split(',')
									position = {
											'X': float(coords[0]),
											'Y': float(coords[1]),
											'Z': float(coords[2])
									}
									break
					result = {'status': status, 'position': position}
					print(result)
				return result
		return {}
	
	def reads(self):
		if self.IsOpen:
			msgs = self.ser.readlines()
			if len(msgs) > 0:
				return msgs
		return None

	def read(self,all = False):
		msg = ""
		if self.IsOpen:
			msg = self.ser.readlines()
			msgs= []
			for text in msg:
				text = text.decode("utf-8")
				text = text.replace('\r\n',str())
				msgs.append(text)
			msg = ','.join(msgs)
		return msg
	
	def onChanged(self, prop):
		if prop in ["Job"]:
			self.__setJob()
		return super().onChanged(prop)
	
	def GetSetingByGrbl(self):
		setting = {}
		cmd = self.send("$$", True)
		if cmd:
			for item in cmd.split(","):
				if item:
					temp = item.split("=")
					if len(temp) == 2:
						name = temp[0]
						value = temp[1]
						setting[name] = value
		self.Setting = setting

	def SetSetingForGrbl(self):
		setting = self.Setting
		cmds = "\n".join(f"{v}={setting[v]}" for  v in setting)
		result = self.send(cmds,True)
		print(cmds,result)


	def get_command(self):
		cmds = super().get_command()
		cmds.extend(["ReConnect", "GetSetingByGrbl", "SetSetingForGrbl"])
		return cmds
	
	def SetD8(self,status=True):
		self.append_job("M7" if status else "M9",isIdle=False)

	def SetD9(self,status=True):
		self.append_job("M8" if status else "M9",isIdle=False)

	def SetD10(self,value):
		self.append_job("M3 S{}".format(value) if value > 0 else "M5",isIdle=False)

main = MainObject()
main.add(ObjectGrbl)


# D8 (Mist Coolant)			M7															M9
# D9 (Flood Coolant)		M8															M9
# D10 (Spindle Enable)	M3 S1000 (CW) / M4 S1000 (CCW)	M5
