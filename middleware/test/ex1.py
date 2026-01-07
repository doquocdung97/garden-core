from django.http import JsonResponse
from core import Core
def test(request):

	document = Core.get('testdemodata')
	if(not document):
		document = Core.create("Document","testdemodata")
		# document.addObserver(observer)

		# document.Parameter.addProperty("PropertyFloatEnum","ParameterFloat")
		# document.Parameter.ParameterFloat = [1.1,2.0,10]
		# document.Parameter.ParameterFloat = 10

		document.Label = "test demo"
		document.addProperty("PropertyObject","base")
		# media = document.addMedia('./README.md',"label requirement")
		# media1 = document.addMedia('./install.bat',"install")
		obj = document.addObject('ObjectBase',"Furture")
		obj1 = document.addObject('ObjectBase',"FurtureTest")
		# obj.Label = "Furture_1 demo test"
		# Furture_1 = document.addObject('ObjectSchedule',"Furture")
		# Furture_1.addProperty("PropertyFloat","Datas")
		# Furture_1.Datas = document.Parameter.ParameterFloat

		# car = document.addObject('ObjectCar',"Car")
		group  = document.addObject('ObjectGroup',"Group")
		# camera = document.addObject("ObjectCameraBase","CameraBase")
		group.Children = [obj,obj1]
		# car.Camera = camera
		
		# obj.addProperty("PropertyStrings","Texts")
		# obj.Texts = ["1","2","3"]

		# obj.addProperty("PropertyObject","base")
		# obj.addProperty("PropertyFloat","Datas")
		# obj.addProperty("PropertyVectors","Vector")
		# obj.addProperty("PropertyMedias","Medias","group","this is list medias",2)
		# obj.addProperty("PropertyColor","Color","group","this is Color",2)
		# obj.addProperty("PropertyDocument","Template")
		# doctestdemo = Core.get('test')
		# if doctestdemo:
		# 	doctestdemo = doctestdemo.clone()
		# 	obj.Template = doctestdemo
		# obj.Color = Color(1,20,40)
		# obj.Vector = [Vector(10,10,10),Vector(10,20,10),Vector(10,30,0.10)]
		# obj.Datas = document.Parameter.ParameterFloat
		# obj.base = Furture_2
		# obj.Medias = [media,media1]
		
		# obj.Time =time(0,0,1)
	# obj2 = document.addObject('ObjectBase',"Furture_3")
	# document.onDelete(obj2)
	result = Core.cmd.run('Vector2D',1,2,"")
	if not document.checkNameInProperty("Base"):
		document.addProperty("PropertyObject","Base")
	
	if not document.Parameter.checkNameInProperty("ParameterFloat"):
		# document.Parameter.addProperty("PropertyStrings","Texts")
		# document.Parameter.Texts = ["1","2","3"]
		document.Parameter.addProperty("PropertyFloatEnum","ParameterFloat")
		document.Parameter.ParameterFloat = [1.1,2.0,10]
		document.Parameter.ParameterFloat = 10

	if not document.Parameter.checkNameInProperty("Text"):
		document.Parameter.addProperty("PropertyStrings","Text")
		document.Parameter.Text = ["1"]

	# main = MainProperty()
	data = {
		# "typeproperty":[name for name in main.get()],
		"document":document.toJSON()
	}
	return JsonResponse(data)
# test(None)