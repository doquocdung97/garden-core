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
def test(request):
    print(request)
    core = Core()
    
    document = core.get('test')
    if(not document):
        document = core.create('test')
        obj = document.addObject('ObjectBase',"Furture_1")
        Furture_2 = document.addObject('ObjectBase',"Furture_2")
        obj.addProperty("PropertyObject","base")
        obj.base = Furture_2
        
    main = MainProperty()
    data = {
        "typeproperty":[name for name in main.get()],
        "document":document.save()
    }
    return JsonResponse(data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test),
]
