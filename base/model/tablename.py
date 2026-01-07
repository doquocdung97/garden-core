class DOCUMENT_TABLE:
  NAME = "db_document"
  ID = "id"
  OBJECTS = "objects"

class OBJECT_TABLE:
  NAME = "db_object"
  ID = "id"
  # DOCUMENT = "document"
  CHILDREN = "children"
  PARENT = "parent"
  PROPERTY = "property"

class PROPERTY_TABLE:
  NAME = "db_property"
  ID = "id"
  OBJECT = "object"