class PropertyBase:
    def __init__(self,obj,name,group,tip,status):
        self.object = obj
        self.__Value = None
        self.__Name = name
        self.group = group
        self.tip = tip
        self.status = status

    @property
    def Value(self):
        return self.getValue()
    @Value.setter
    def Value(self,val):
        if self.checkValue(val):
            if self.getValue() != val:
                self.object.onBeforeChange(self.__Name)
                self.setValue(val)
                self.object.onChanged(self.__Name)
                self.object.setChange(True)
        else:
            raise ValueError('not value type')
    def getType(self):
        return self.__class__.__name__
    def save(self,reader = None):
        return {
            'name': self.__Name,
            'type': self.__class__.__name__,
            'value':self.getValue(True),
            'group': self.group,
            'tip': self.tip,
            'status': self.status
        }
    def restore(self,reader = None):
        self.setValue(reader.dataRestore['value'])
        pass
    def getValue(self,isSave = False):
        return self.__Value
    def checkValue(self,val):
        return True
    def setValue(self,val):
        self.__Value = val
        

    # def __repr__(self):
    #     if hasattr(self,'toString'):
    #         return str(self.toString())
    #     return self

class MainProperty():
    instance = None
    properties = {}

    def __init__(self):
        # super().__init__()
        if(MainProperty.instance):
            return MainProperty.instance
        MainProperty.instance = self

    def get(self,name:str)->PropertyBase|None:
        return self.properties[name]
    def get(self)->list[PropertyBase]:
        return self.properties

    def add(self,name,property)->bool:
        items = self.getItems()
        if not name in items:
            self.properties[name] = property()
            return True
        return False
