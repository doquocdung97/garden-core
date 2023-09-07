from base.document import Document,_MainDocument
from base.object import ObjectBase
main = _MainDocument()

class DocumentTree(Document):
	def __init__(self):
		super(DocumentTemplateTree,self).__init__()

	def setProperties(self):
		super(DocumentTemplateTree,self).setProperties()
		if not "Height" in self.propertys:
			self.addProperty("PropertyFloat","Height")
			self.Height = 100
		if not "Width" in self.propertys:
			self.addProperty("PropertyFloat","Width")
			self.Width = 100
	def init(self):
		# if not hasattr(self,"GroupTree"):
		# 	super(DocumentTemplateTree,self).addObject("ObjectGroup", "GroupTree")
		super(DocumentTemplateTree,self).init()
		# self.__log.info("test data")
	def addObject(self, type, name) -> ObjectBase | None:

		obj = super().addObject(type, name)
		# if type == "ObjectTree":
		# 	child = self.GroupTree.Child
		# 	child.append(obj)
		# 	self.GroupTree.Child = child

		return obj

class DocumentTemplateTree(Document):
	def __init__(self):
		super(DocumentTemplateTree,self).__init__()

	def setProperties(self):
		super(DocumentTemplateTree,self).setProperties()
		if not self.checkNameInProperty("Radius"):
			self.addProperty("PropertyFloat","Radius")

main.add(DocumentTree)
main.add(DocumentTemplateTree)