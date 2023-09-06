from common.filehelper import FileHelper
from common.loggerhelper import loggerHelper
from common import createAttribute
from ..property import MainProperty
from ..object import MainObject,ObjectBase
import uuid,tempfile,os,json
from core._version import __project__, __version__
from ..media import Media
from zipfile import ZipFile

class Document:
    def __init__(self):
        self.__isChange = False
        self.__objects = []
        self.__propertys = []
        self.__historys = []
        self.__medias:list[Media] = []
        self.__filename = None
        self.__isTransaction = False
        self.UUID = str(uuid.uuid4())
        self.__name = str()
        self.__tempdir = os.path.join(tempfile.gettempdir(),__project__,str(uuid.uuid4()))

    def init(self):
        self.__log = loggerHelper(str(self))
    @property
    def Name(self):
        return self.__name
    
    @Name.setter
    def Name(self,val:str):
        if isinstance(val,str):
            self.__name = val
        else:
            raise ValueError("value not type string")

    def setProperties(self):
        if not "Label" in self.__propertys:
            self.addProperty('PropertyString','Label')
    @property
    def TempDir(self):
        tempdir = self.__tempdir
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        return tempdir

    def openTransaction(self,name):
        pass

    def commitTransaction(self):
        pass
    
    @property
    def Objects(self)->list[ObjectBase]:  
        return self.__objects
    
    @property
    def Medias(self)->list[Media]:
        return self.__medias
    
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
        main_property = MainProperty()
        property = main_property.get(type)
        if property:
            name = createAttribute(self,name)
            property = property(self,name,group,tip,status,type)
            self.__dict__[name] = property
            self.__propertys.append(name)
            return True
        return None
    
    def addObject(self,type,name) ->ObjectBase|None:
        mainobject = MainObject()
        object = mainobject.get(type)
        if object:
            object:ObjectBase = object(self)
            object.setProperties()
            name = createAttribute(self,name)
            object.Name = name
            self.__dict__[name] = object
            self.__objects.append(object)
            self.__isChange = True
            object.init()
            return object
        return None
    
    def addMedia(self,path:str,name:str = None)->Media|None:
        file = FileHelper(path)
        if file.isNone():
            file_name = file.toFileName(True)
            file.copy(os.path.join(self.TempDir,file_name))
            media = Media(self,file_name)
            if name:
                media.Name = name
            self.__medias.append(media)
            return media
    
    def getMediaByName(self,name:str):
        for media in self.__medias:
            if media.Name == name:
                return media
        return None
    
    def getMediaByUUID(self,uuid:str):
        for media in self.__medias:
            if media.UUID == uuid:
                return media
        return None
    
    def isChange(self):
        return self.__isChange
    def setChange(self,status):
        self.__isChange = status

    @property
    def FileName(self):
        # return self.__filename
        return f"{self.__name}.zip"
    
    @FileName.setter
    def FileName(self,val):
        self.__filename = val

    def save(self):
        try:
            self.__isChange = False
            with ZipFile(self.FileName,'w') as zf:
                data = self.toJSON()
                with zf.open("data.json", "w") as c:
                    c.write(json.dumps(data, indent=2).encode("utf-8"))
                for media in self.__medias:
                    zf.write(media.PathFile,media.FileName)
                zf.close()
            return self.toJSON()
        except Exception as ex:
            self.__log.error(f"save document error: {ex}")
    def toJSON(self):
        # if not self.FileName:
        #     if not self.saveAs():
        #         return
        propertys = []
        reader = {'file':[]}
        for property in self.__propertys:
            dataproperty = self.__dict__[property].save(reader)
            propertys.append(dataproperty)
        objects = []
        for object in self.Objects:
            content = object.save(reader)
            objects.append(content)

        medias = []
        for media in self.__medias:
            mediajson = media.toJSON()
            medias.append(mediajson)
        data = {
            "name":self.Name,
            "version":__version__,
            "type":self.__class__.__name__,
            'uuid':self.UUID,
            'propertys':propertys,
            'medias': medias,
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

    def __restoreObject(self,data):
        type = data['type']
        name = data['name']
        if not hasattr(self,name):
            mainobject = MainObject()
            object = mainobject.get(type)
            if object:
                object:ObjectBase = object(self)
                object.onDocumentRestoredBefore(data)
                # object.restore(data)
                self.__dict__[name] = object
                self.__objects.append(object)
                object.init()
                return (object,data)
    
    def restore(self,render):
        try:
            self.__tempdir = render['tempdir']
            self.UUID = render['uuid']
            self.Name = render['name']
            for property in render['propertys']:
                self.addProperty(property['type'],property['name'],property['group'],property['tip'],property['status'])
                if property['name'] in self.__propertys:
                    self.__dict__[property['name']].restore(property)

            objs = []
            for object in render['objects']:
                data = self.__restoreObject(object)
                objs.append(data)
            for obj in render["medias"]:
                media = Media.parse(self,obj)
                # pathfile = media["pathfile"]
                # uuid = media["uuid"]
                # media = Media(self,pathfile,uuid)
                self.__medias.append(media)

            for obj,data in objs:
                obj.restore(data)
                obj.onDocumentRestoredAfter(data)

        except Exception as ex:
            self.__log.error(f"restore document error: {ex}")
            
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

    def execute(self):
        for obj in self.Objects:
            if obj.IsChange:
                obj.execute()

    def onBeforeChange(self,prop):
        pass
    def onChanged(self, prop):
        pass
    def getObjectByName(self,name:str)->ObjectBase|None:
        obj = self.__dict__.get(name)
        if isinstance(obj,ObjectBase):
            return obj
        
    def getObjectByUUID(self,uuid:str)->ObjectBase|None:
        for obj in self.Objects:
            if obj.UUID == uuid:
                return obj
        return None
        
    def deleteObject(self,obj:ObjectBase):
        if(self.getObjectByName(obj.Name)):
            if obj.onDelete():
                delattr(self,obj.Name)
                self.__objects.remove(obj)
    def deleteMedia(self,media:Media):
        media.onDelete()
        self.__medias.remove(media)
    def onDelete(self):
        for index in range(len(self.__medias)):
            media = self.__medias[0]
            self.deleteMedia(media)
        for index in range(len(self.__objects)):
            obj = self.__objects[0]
            self.deleteObject(obj)

        file = FileHelper(self.TempDir)
        file.deleteDir()
    def __repr__(self):
        return str(f"{self.__class__.__name__}({self.Name})")
class _MainDocument:
    __documents = {}

    def add(self, doc:Document):
        name = doc.__name__
        if isinstance(doc,Document):
            raise TypeError("it is not type the Document.")
        if not name in self.__documents:
            self.__documents[name] = doc
        else:
            raise ValueError(f"name: {name} is already in the data")
    def get(self,name:str = None)->dict|Document|None:
        if name:
            return self.__documents.get(name)
        return self.__documents
    
main = _MainDocument()
main.add(Document)