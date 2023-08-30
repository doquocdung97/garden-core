from base.document import Document
import mod
class Core():
    instance = None 
    documents = {}

    def __init__(self):
        self.mod = mod.module
        # super().__init__()
        if(Core.instance):
            self =  Core.instance
        else:
            Core.instance = self

    # def __init__(self):
    #     # super().__init__()
    #     main = {}
    #     name = type(self).__name__ + str(id(type(self).__name__))
    
    #     try:
    #         if(globals().get(name)):
    #             main = globals().get(name)
    #         else:
    #             globals()[name] = self
    #             main = globals()[name]
    #     except:
    #         main = {}
    #     return main
    
    def get(self,name:str = None)->list[Document]|Document|None:
        if not name:
            return self.documents
        return self.documents.get(name)

    def create(self,name)->Document|None:
        if not name in self.documents:
            self.documents[name] = Document()
            return self.documents.get(name)
        return None