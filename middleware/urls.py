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
# from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from core import Core
from base.property import MainProperty
from datetime import time
from base.common import Vector, Color
from common import get_temp_dir
from base.document import _MainDocument
from base.object import MainObject
import os,json
from graphene_django.views import GraphQLView
from graphene_file_upload.django  import FileUploadGraphQLView
 
from .graphql import schema
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from .test.ex1 import test 
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

from django.http import FileResponse, Http404
# from django.contrib.staticfiles.finders import find

def serve_static_file(request,doc, path):
		doc = Core.get(doc)
		if doc:
			file = doc.get_media_with_path(path)
			if file:
				response = FileResponse(file.open())
				response['Cache-Control'] = 'public, max-age=86400'
				return response
			
		raise Http404(f"Static file '{path}' not found.")
						
urlpatterns = [
	path('test/', test),
	path('command/', command),
	path('restore/', restore),
	path('save/', save),
	path('clone/', clone),
	path('config/', config),
	# path('camera/', livefe, name="live_camera"),
	path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=False,schema=schema)),name="graphql"),
	path('media/<str:doc>/<path:path>', serve_static_file),
	# path('', index),
]