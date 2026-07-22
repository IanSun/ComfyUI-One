from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	value: bool

class OneBoolean(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneBoolean",
			category = "One/Primitive",
			inputs = [
				io.Boolean.Input(
					id = "value",
					default = False,
				),
			],
			outputs = [
				io.Int.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		value = bool(kwargs["value"])

		return io.NodeOutput(value)
