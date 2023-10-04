from graphene.types.scalars import Scalar

class ObjectField(Scalar):
   ''' convert the Json String into Json '''
   @staticmethod
   def serialize(dt):
      return dt

   @staticmethod
   def parse_literal(node):
      return node.value

   @staticmethod
   def parse_value(value):
      return value