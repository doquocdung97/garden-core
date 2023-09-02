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
from base.common import Vector
import os,json
def test(request):
	
	document = Core.get('test')
	if(not document):
		document = Core.create("Document","test")
		obj = document.addObject('ObjectSchedule',"Furture_1")
		Furture_2 = document.addObject('ObjectBase',"Furture_2")
		Furture_2.Label = "demo test"
		obj.addProperty("PropertyStrings","Texts")
		obj.Texts = ["1","2","3"]

		obj.addProperty("PropertyObject","base")
		obj.addProperty("PropertyFloatEnum","Datas")
		obj.addProperty("PropertyVectors","Vector")
		obj.Vector = [Vector(10,10,10),Vector(10,20,10),Vector(10,30,0.10)]
		obj.Datas = [1.1,2.0,0.0]
		obj.base = Furture_2
		obj.Time =time(0,0,1)
	# obj2 = document.addObject('ObjectBase',"Furture_3")
	# document.onDelete(obj2)
	result = Core.cmd.runCommand('Vector2D',1,2,"")
	print(result)
	main = MainProperty()
	data = {
		"typeproperty":[name for name in main.get()],
		"document":document.save()
	}
	return JsonResponse(data)
# test(None)
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
	path = os.path.abspath("./backup")
	file_name = "data.json"
	doc = Core.get("test")
	data = {}
	if doc:
		data = doc.save()
		try:
			with open(os.path.join(path,file_name), "w") as json_file:
				# Write the data to the file in JSON format
				json.dump(data, json_file)
		finally:
			json_file.close()
	return JsonResponse(data)

def restore(request):
	path = os.path.abspath("./backup")
	file_name = "data.json"
	data = {}
	try:
		with open(os.path.join(path,file_name), "r") as json_file:
			data = json.load(json_file)
			Core.restore(data)
	finally:
		json_file.close()
	return JsonResponse(data)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('test/', test),
	path('update/', update),
	path('command/', command),
	path('restore/', restore),
	path('save/', save),
]
