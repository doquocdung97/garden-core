from base import Property

class ObjectBase:
    
    def __init__(self,document):
        self.__document = document
        self.__isChange = False
        self.__propertys = []
        self.addProperty('PropertyString','Name')
        self.addProperty('PropertyString','Label')
        pass

    def save(self,reader):
        propertys = []
        for property in self.__propertys:
            dataproperty = self.__dict__[property].save(reader)
            propertys.append(dataproperty)

        return {
            'type':self.__class__.__name__,
            'name':self.Name, 
            'propertys':propertys
        }
        
    def restore(self,reader):
        propertys = reader.dataRestore
        for property in propertys:
            self.addProperty(property['type'],property['name'],property['group'],property['tip'],property['status'])
            if property['name'] in self.__propertys:
                reader.dataRestore = property
                self.__dict__[property['name']].restore(reader)
    

    def isChange(self):
        return self.__isChange
    def setChange(self,status):
        self.__isChange = status
    @property
    def Document(self):
        return self.__document
    @property
    def propertys(self):
        return self.__propertys

    def onDocumentRestored(self,obj):
        pass
    def addProperty(self,type,name,group = '',tip = '',status = 1):
        if not hasattr(self,name):
            property = Property.getproperty(type)
            if property:
                property = property(self,name,group,tip,status)
                self.__dict__[name] = property
                self.__propertys.append(name)
    def __setattr__(self, name, value):
        if hasattr(self,name) and name in self.__propertys:
            self.__dict__[name].Value = value
            return
        return super().__setattr__(name, value)

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name).Value
        except:
            return super().__getattribute__(name)

    def setExecute(self):
        self.__document.setChange(True)
        self.execute()
        self.setChange(False)

    def execute(self):
        pass
    def onBeforeChange(self,prop):
        pass
    def onChanged(self, prop):
        pass
    def __repr__(self):
        return self.__class__.__name__ + "({0})".format(self.Name)