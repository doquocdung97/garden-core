from core import Core,Command,Schedule
from core.schedule import EveryDay, EveryTime
from common import loggerHelper
import datetime, threading,schedule
from datetime import time
from base.object.common import MainObject, ObjectBase
# class _ScheduleTest(Schedule):
#     def __init__(self) -> None:
#         super().__init__()
#     def Time(self) -> EveryDay | EveryTime:
#         return EveryTime(1)
#     def Activated(self):
#         self.logger.info("test schedule")
				
# Core.schedule.add(_ScheduleTest())
class ObjectSchedule(ObjectBase):
		def __init__(self, document):
				super().__init__(document)
				# self.threading = threading.Thread(target=self.loop,daemon=True)
				
		def init(self):
				super().init()


		def setProperties(self):
				if not "Type" in self.propertys:
						self.addProperty("PropertyStringEnum","Type")
						self.Type = ["EVERYDAY","EVERYTIME"]
						self.Type = "EVERYTIME"
				if not "Time" in self.propertys:
						self.addProperty("PropertyTime","Time")
						self.Time = time(0,1)
				return super().setProperties()
		def onDocumentRestoredAfter(self, reader: dict):
				self.setJob()
				return super().onDocumentRestoredAfter(reader)
		def setJob(self):
				if hasattr(self,"job"):
						schedule.cancel_job(self.job)

				if  hasattr(self,"Type") and hasattr(self,"Time"):
						time_val:time = self.Time
						if self.Type == "EVERYDAY":
								self.job = schedule.every().day.at(f"{time_val.hour}:{time_val.minute}").do(self.execute)
						else:
								if(time_val.minute > 0):
										self.job = schedule.every(time_val.minute).minutes.do(self.execute)
								elif (time_val.second > 0):
										self.job = schedule.every(time_val.second).seconds.do(self.execute)
		#     self.threading.start()
				
		# def loop(self):
		#     while True:
		#         self.job.run()
		#         time.sleep(1)
		#         self.logger.info("loop")
		def onDelete(self):
				if hasattr(self,"job"):
						schedule.cancel_job(self.job)
				return super().onDelete()

		def execute(self):
				self.logger.info("execute")
				return super().execute()

		def onChanged(self, prop):
				super().onChanged(prop)
				if prop in ["Time","Type"]:
						self.setJob()

main = MainObject()
main.add(ObjectSchedule)