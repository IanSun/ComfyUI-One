from comfy_api.latest import io
from typing import TypedDict, Unpack

class OneIntInputs(TypedDict):
	value: int

class OneInt(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneInt",
			category = "One/Primitive",
			inputs = [
				io.Int.Input(
					id = "value",
					default = 0,
					socketless = True,
				),
			],
			outputs = [
				io.Int.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntInputs]) -> io.NodeOutput:
		return io.NodeOutput(kwargs["value"])
