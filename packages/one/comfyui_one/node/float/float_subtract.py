from comfy_api.latest import io
from decimal import Decimal
from typing import TypedDict, Unpack

class OneFloatSubtractInputs(TypedDict):
	minuend: float | int
	subtrahend: float | int

class OneFloatSubtract(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatSubtract",
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
				io.Float.Output(id = "difference"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatSubtractInputs]) -> io.NodeOutput:
		return io.NodeOutput(float(Decimal(str(kwargs["minuend"])) - Decimal(str(kwargs["subtrahend"]))))
