"""
URL configuration for middleware project.

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from core import Core
from base.property import MainProperty
from datetime import time
from base.common import Vector, Color
from base.document import _MainDocument
from base.object import MainObject
import os,json
from graphene_django.views import GraphQLView
from .graphql import schema
from django.views.decorators.csrf import csrf_exempt
# class Observer:
# 	# def onBeforeChange(self,doc,prop):
# 	# 	print("onBeforeChange - onBeforeChange  ",doc, prop)
		
# 	# def onChanged(self,doc,prop):
# 	# 	print("Observer - onChanged  ",doc, prop)

# 	# def onChangedObject(self,doc,obj, prop:str):
# 	# 	print("Observer - onChangedObject  ",doc,obj, prop)

# 	def allObserver(self,doc,*args, **kwds):
# 		print("Observer - allObserver  ",doc,*args, **kwds)

# observer = Observer()
def test(request):

	document = Core.get('testdemo')
	if(not document):
		document = Core.create("Document","testdemo")
		# document.addObserver(observer)

		document.Parameter.addProperty("PropertyFloatEnum","ParameterFloat")
		document.Parameter.ParameterFloat = [1.1,2.0,10]
		document.Parameter.ParameterFloat = 10

		document.Label = "test demo"
		# media = document.addMedia('./README.md',"label requirement")
		# media1 = document.addMedia('./install.bat',"install")
		# obj = document.addObject('ObjectBase',"Furture")
		# obj.Label = "Furture_1 demo test"
		# Furture_1 = document.addObject('ObjectSchedule',"Furture")
		# Furture_1.addProperty("PropertyFloat","Datas")
		# Furture_1.Datas = document.Parameter.ParameterFloat

		car = document.addObject('ObjectCart',"Car")
		camera = document.addObject("ObjectCameraBase","CameraBase")

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
	# main = MainProperty()
	data = {
		# "typeproperty":[name for name in main.get()],
		"document":document.toJSON()
	}
	return JsonResponse(data)
test(None)
def update(request):
	time = request.GET.get('time', None)
	document = Core.get('test')
	if document and time:
		document.Furture_1.Time = int(time)
	return JsonResponse({"time":time})
def command(request):
	cmd = request.GET.get('cmd', None)
	valset = request.GET.get('set', False)
	try:
		e = None
		if valset:
			exec(cmd)
		else:
			e = eval(cmd)
		e = str(e)
	except Exception as ex:
		e = str(ex)

	return JsonResponse({
		"command":cmd,
		"result":e
		})
def save(request):
	name = request.GET.get('name', "test.zip")
	path = os.path.join("./backup",name)
	# file_name = "data.json"
	doc = Core.get("testdemo")
	data = {}
	if doc:
		data = doc.saveAs(os.path.abspath(path))
		# try:
		# 	with open(os.path.join(path,file_name), "w") as json_file:
		# 		# Write the data to the file in JSON format
		# 		json.dump(data, json_file)
		# finally:
		# 	json_file.close()
	return JsonResponse(data)

def restore(request):
	path = request.GET.get('path', "")
	path = os.path.abspath(path)
	doc = Core.restore(path)
	return JsonResponse(doc.toJSON())

def config(request):
	main = MainProperty()
	maindoc = _MainDocument()
	mainobj = MainObject()
	data = {
		"command":[name for name in Core.cmd.get()],
		"typedocument":[name for name in maindoc.get()],
		"typeobject":[name for name in mainobj.get()],
		"typeproperty":[name for name in main.get()],
	}
	return JsonResponse(data)

def clone(request):
	name = request.GET.get('name', "testdemo")
	doc = Core.get(name)
	data = {}
	if doc:
		doc = doc.clone()
		data = doc.toJSON()
		# try:
		# 	with open(os.path.join(path,file_name), "w") as json_file:
		# 		# Write the data to the file in JSON format
		# 		json.dump(data, json_file)
		# finally:
		# 	json_file.close()
	return JsonResponse(data)

# from .camera import livefe
# from django.http import HttpResponse
# from django.template import Context, loader
# def index(request):
#     template = loader.get_template('index.html')
#     return HttpResponse(template.render({}, request))

urlpatterns = [
	path('admin/', admin.site.urls),
	path('test/', test),
	path('update/', update),
	path('command/', command),
	path('restore/', restore),
	path('save/', save),
	path('clone/', clone),
	path('config/', config),
	# path('camera/', livefe, name="live_camera"),
	path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=False,schema=schema)),name="graphql"),
	# path('', index),
]