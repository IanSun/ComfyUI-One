from comfy_api.latest import io
from typing import TypedDict, Unpack

class OneIntSubtractInputs(TypedDict):
	minuend: int
	subtrahend: int

class OneIntSubtract(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntSubtract",
			category = "One/Math",
			inputs = [
				io.Int.Input(
					id = "minuend",
					default = 0,
				),
				io.Int.Input(
					id = "subtrahend",
					default = 0,
				),
			],
			outputs = [
				io.Int.Output(id = "difference"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntSubtractInputs]) -> io.NodeOutput:
		return io.NodeOutput(kwargs["minuend"] - kwargs["subtrahend"])
