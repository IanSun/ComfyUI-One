from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	minuend: float | int
	subtrahend: float | int

class OneIntSubtract(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntSubtract",
			category = "One/Math",
			inputs = [
				io.MultiType.Input(
					id = "minuend",
					types = [
						io.Float,
						io.Int,
					],
				),
				io.MultiType.Input(
					id = "subtrahend",
					types = [
						io.Float,
						io.Int,
					],
				),
			],
			outputs = [
				io.Int.Output(id = "difference"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		difference = int(kwargs["minuend"] - kwargs["subtrahend"])

		return io.NodeOutput(difference)
