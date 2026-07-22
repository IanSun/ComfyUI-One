from comfy_api.latest import io
from typing import TypedDict, Unpack

class OneFloatInputs(TypedDict):
	value: float

class OneFloat(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloat",
			category = "One/Primitive",
			inputs = [
				io.Float.Input(
					id = "value",
					default = 0.0,
					socketless = True,
				),
			],
			outputs = [
				io.Float.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatInputs]) -> io.NodeOutput:
		return io.NodeOutput(kwargs["value"])
