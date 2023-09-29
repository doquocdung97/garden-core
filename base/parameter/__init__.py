from base.property import HanlderProperty
class Parameter(HanlderProperty):
	def __init__(self) -> None:
		super().__init__()

	def onChanged(self, prop):
		return super().onChanged(prop)
	