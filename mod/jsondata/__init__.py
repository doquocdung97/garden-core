from base.property.common import *
import os
main = MainProperty()

class PropertyJson(PropertyBase):
    def valueDefault(self):
        return {}
    def checkValue(self,vals):
        for val in vals:
            if isinstance(val,dict):
                return False
        return True
main.add(PropertyJson)