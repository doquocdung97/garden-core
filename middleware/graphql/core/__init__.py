import graphene
from .schema import ResultCommand,BaseResultCode,Command,Config
from ..common.scalar import ObjectField
from core import Core,IsNone
from base.document import _MainDocument
from base.object import MainObject
from base.property import MainProperty

class _Mutation(graphene.ObjectType):
	runCommand = graphene.Field(ResultCommand,
														 name=graphene.Argument(graphene.String,required=True),
														 document=graphene.Argument(graphene.String),
														 parameters=graphene.Argument(graphene.List(ObjectField))
														 )
	
	def resolve_runCommand(root, info,name,document = None,parameters = []):
		model = ResultCommand()
		try:
			cmd = Core.cmd.get(name)
			if cmd:
				params = []
				for param in parameters:
					if isinstance(param,dict):
						if param.get("type") in ["object","media"]:
							doc = None
							if document:
								doc = Core.get(document)
							if doc:
								mode = doc.getMode(param.get("type"))
								obj = mode.getObjectByName(param.get("name"))
								if obj:
									params.append(obj)
								else:
									params.append(None)
							else:
								params.append(None)
						elif param.get("type") == "document":
							doc = None
							if param.get("name"):
								doc = Core.get(param.get("name"))
								if doc:
									params.append(doc)
							else:
								raise ValueError('not found document')
					else:
						params.append(param)
				model.data = Core.cmd.run(name,*params)
			else:
				model.success = False
				model.code = BaseResultCode.B002
		except Exception as ex:
			model.success = False
			model.code = BaseResultCode.B005
			model.message = str(ex)
		return model
	
class _Query(graphene.ObjectType):
	commands = graphene.Field(graphene.List(Command))
	config = graphene.Field(Config)
	
	def resolve_commands(root, info):
		rowdatas = []
		for cmd in Core.cmd.get():
			data = Core.cmd.get(cmd)
			resources = data.GetResources()
			rowdata = Command()
			rowdata.name = cmd
			rowdata.title = resources.get('Title')
			rowdata.tooltip = resources.get('Tooltip')
			params = data.Parameter()
			rowdata.args = []
			if params and len(params) > 0:
				args = []
				for obj in data.Parameter():
					if isinstance(obj,IsNone):
						args.append(obj.Meta.__name__ )
					else:
						args.append(obj.__name__)
				rowdata.args = args
			rowdatas.append(rowdata)
		return rowdatas
	
	def resolve_config(root, info):
		rowdatas = []
		for cmd in Core.cmd.get():
			data = Core.cmd.get(cmd)
			resources = data.GetResources()
			rowdata = Command()
			rowdata.name = cmd
			rowdata.title = resources.get('Title')
			rowdata.tooltip = resources.get('Tooltip')
			params = data.Parameter()
			rowdata.args = []
			if params and len(params) > 0:
				args = []
				for obj in data.Parameter():
					if isinstance(obj,IsNone):
						args.append(obj.Meta.__name__ )
					else:
						args.append(obj.__name__)
				rowdata.args = args
			rowdatas.append(rowdata)
		mainproperty = MainProperty()
		maindoc = _MainDocument()
		mainobj = MainObject()
		data = Config()
		data.command = rowdatas
		data.document = [name for name in maindoc.get()]
		data.object = [name for name in mainobj.get()]
		data.property = [name for name in mainproperty.get()]
		return data
	
schema_core = graphene.Schema(
		mutation=_Mutation,
		query=_Query
)