from comfy_api.latest import io
from typing import TypedDict, Unpack

class OneBooleanInputs(TypedDict):
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
					socketless = True,
				),
			],
			outputs = [
				io.Boolean.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneBooleanInputs]) -> io.NodeOutput:
		return io.NodeOutput(kwargs["value"])
