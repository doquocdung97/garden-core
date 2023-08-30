from ..property import MainProperty
from ..object import MainObject,ObjectBase
import uuid,tempfile,os,json

class Document:
    def __init__(self):
        self.__isChange = False
        self.__objects = []
        self.__propertys = []
        self.__historys = []
        self.__filename = None
        self.__isTransaction = False
        self.UUID = str(uuid.uuid4())
        self.setProperties()

    def setProperties(self):
        if not "Name" in self.__propertys:
            self.addProperty('PropertyString','Name')
        if not "Label" in self.__propertys:
            self.addProperty('PropertyString','Label')
        pass
    # @property
    # def TempDir(self):
    #     tempdir = os.path.join(tempfile.gettempdir(),__Project__ + self.UUID)
    #     if not os.path.exists(tempdir):
    #         os.makedirs(tempdir)
    #     return tempdir

    def openTransaction(self,name):
        pass

    def commitTransaction(self):
        
        pass
    
    @property
    def Objects(self):  
        return self.__objects
    
    def close(self):
        if os.path.exists(self.TempDir):
            import shutil
            shutil.rmtree(self.TempDir)

    # @attr.setter
    # def attr(self, value):
    #     self.__attr = value
    # def Objects(self):
    #     return self.__objects
    def addProperty(self,type,name,group = '',tip = '',status = 1)->bool:
        if not hasattr(self,name):
            main_property = MainProperty()
            property = main_property.get(type)
            if property:
                property = property(self,name,group,tip,status,type)
                self.__dict__[name] = property
                self.__propertys.append(name)
                return True
        return False
    
    def addObject(self,type,name) ->ObjectBase|None:
        if not hasattr(self,name):
            mainobject = MainObject()
            object = mainobject.get(type)
            if object:
                object = object(self)
                object.Name = name
                self.__dict__[name] = object
                self.__objects.append(object)
                self.__isChange = True
                return object
        return None
    
    def isChange(self):
        return self.__isChange
    def setChange(self,status):
        self.__isChange = status

    @property
    def FileName(self):
        return self.__filename
    @FileName.setter
    def FileName(self,val):
        self.__filename = val

    def save(self):
        # if not self.FileName:
        #     if not self.saveAs():
        #         return
        self.__isChange = False
        propertys = []
        reader = {'file':[]}
        for property in self.__propertys:
            dataproperty = self.__dict__[property].save(reader)
            propertys.append(dataproperty)
        objects = []
        for object in self.Objects:
            content = object.save(reader)
            objects.append(content)
        data = {
            'uuid':self.UUID,
            'propertys':propertys,
            'objects': objects
        }
        return data
        # with ZipFile(self.FileName,'w') as zf:
        #     with zf.open("data.json", "w") as c:
        #         c.write(json.dumps(data, indent=2).encode("utf-8"))
        #     for file in reader['file']:
        #         zf.write(file,os.path.basename(file))
        #     zf.close()
        # pass
    
    # def saveAs(self,filename = None):
    #     if not filename:
    #         fname = QFileDialog.getSaveFileName(Gui.getMainWindow(), 'save file', '',"Image files (*.zip)")
    #         filename = fname[0]
    #     if not filename:
    #         return False
    #     self.FileName = filename
     

    # def restore(self):
    #     with ZipFile(self.FileName,'r') as reader:
    #         reader.dataRestore = None
    #         files = reader.namelist()
    #         if 'data.json' in files:
    #             files.remove('data.json')
    #             b_data = reader.read('data.json')
    #             jdata = json.loads(b_data)
    #             for property in jdata['propertys']:
    #                 self.addProperty(property['type'],property['name'],property['group'],property['tip'],property['status'])
    #                 if property['name'] in self.__propertys:
    #                     reader.dataRestore = property
    #                     self.__dict__[property['name']].restore(reader)

    #             for object in jdata['objects']:
    #                 obj = self.addObject(object['type'],object['name'])
    #                 if obj:
    #                     reader.dataRestore = object['propertys']
    #                     obj.restore(reader)
    #                 pass
    #             for filename in files:
    #                 file = reader.read(filename)
    #                 filename = os.path.join(self.TempDir,filename)
    #                 f = open(filename, 'wb')
    #                 f.write(file)
    #                 f.close()
    #         reader.close()


    def __setattr__(self, name, value):
        if hasattr(self,name) and name in self.__propertys:
            self.__dict__[name].Value = value
            return
        if hasattr(self,name) and self.__getattribute__(name) in self.__objects:
            raise ValueError("not set attr.")
        return super().__setattr__(name, value)
    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name).Value
        except:
            return super().__getattribute__(name)


    def onBeforeChange(self,prop):
        pass
    def onChanged(self, prop):
        pass