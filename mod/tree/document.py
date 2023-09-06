from base.document import Document,_MainDocument
class DocumentTemplateTree(Document):
	def __init__(self):
		super().__init__()
main = _MainDocument()
main.add(DocumentTemplateTree)