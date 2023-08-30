class PropertyBase:
    def __init__(self, obj, name, group, tip, status, type):
        self.object = obj
        self.__Name = name
        self.__type = type
        self.group = group
        self.tip = tip
        self.status = status
        self.__Value = self.valueDefault()

    def valueDefault(self):
        return None

    @property
    def Value(self):
        return self.getValue()

    @Value.setter
    def Value(self, val):
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

    def save(self, reader=None):
        return {
            'name': self.__Name,
            'type': self.__type,
            'value': self.getValue(True),
            'group': self.group,
            'tip': self.tip,
            'status': self.status
        }

    def restore(self, reader=None):
        self.setValue(reader.dataRestore['value'])
        pass

    def getValue(self, isSave=False):
        return self.__Value

    def checkValue(self, val):
        return True

    def setValue(self, val):
        self.__Value = val

    def toString(self):
        return self.__Value

    def __repr__(self):
        return str(f'{self.__class__.__name__}({self.toString()})')
    #     return self


def PropertyListBase(target):
    name = f'{target.__name__}s'
    class PropertyListBase(target):
        def valueDefault(self):
            return []

        def checkValue(self, vals):
            for val in vals:
                if not super().checkValue(val):
                    return False
            return True

        def __repr__(self):
            return str(f'{name}({self.toString()})')

    return PropertyListBase


class MainProperty():
    instance = None
    properties = {}

    def __init__(self):
        # super().__init__()
        if (MainProperty.instance):
            self = MainProperty.instance
        else:
            MainProperty.instance = self

    def get(self, name: str = None) -> list[PropertyBase] | PropertyBase | None:
        if not name:
            return self.properties
        return self.properties.get(name)
    # def get(self)->list[PropertyBase]:
    #     return self.properties

    def addHasList(self, property: type) -> bool:
        name = property.__name__
        if issubclass(property, PropertyBase):
            datas = [
                (name,property),
                (f'{name}s',PropertyListBase(property)),
            ]
            for item in datas:
                if not item[0] in self.properties:
                    self.properties[item[0]] = item[1]
            return True
        return False
    
    def add(self, property: type) -> bool:
        name = property.__name__
        if issubclass(property, PropertyBase) and not name in self.properties:
            self.properties[name] = property
            return True
        return False