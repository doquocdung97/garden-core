from .database import create_db_engine, get_declarative_base
from .document import *
from .object import *
from .property import *

engine = create_db_engine()
base = get_declarative_base()
base.metadata.create_all(engine)

# post = Document(name="test",objects = [])
# comment1 = Object(name="test 1")
# comment2 = Object(name="Thanks for sharing!")
# comment1.children = [comment2]
# post.objects = [comment1,comment2]
# session = create_db_session(engine)
# session.add(comment1)
# session.commit()
# parent_obj = Object(name="Parent")
# child_obj = Object(name="Child", parent=parent_obj)

# session.add(parent_obj)

# comment1 = ObjectModel(name="test 1 2")
# comment2 = ObjectModel(name="Thanks for sharing! 2")
# comment1.children = [comment2]
# session.add(comment1)
# session.commit()