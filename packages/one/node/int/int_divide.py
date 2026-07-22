from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	dividend: float | int
	divisor: float | int

class OneIntDivide(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntDivide",
			category = "One/Math",
			inputs = [
				io.MultiType.Input(
					id = "dividend",
					types = [
						io.Float,
						io.Int,
					],
				),
				io.MultiType.Input(
					id = "divisor",
					types = [
						io.Float,
						io.Int,
					],
				),
			],
			outputs = [
				io.Int.Output(id = "quotient"),
				io.Int.Output(id = "remainder"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		quotient = int(kwargs["dividend"] // kwargs["divisor"])
		remainder = int(kwargs["dividend"] % kwargs["divisor"])

		return io.NodeOutput(
			quotient,
			remainder,
		)
