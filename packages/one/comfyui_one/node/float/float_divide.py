from comfy_api.latest import io
from decimal import Decimal
from typing import TypedDict, Unpack

class OneFloatDivideInputs(TypedDict):
	dividend: float | int
	divisor: float | int

class OneFloatDivide(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatDivide",
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
				io.Float.Output(id = "value"),
				io.Int.Output(id = "quotient"),
				io.Float.Output(id = "remainder"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatDivideInputs]) -> io.NodeOutput:
		dividend = Decimal(str(kwargs["dividend"]))
		divisor = Decimal(str(kwargs["divisor"]))

		quotient, remainder = divmod(dividend, divisor)

		return io.NodeOutput(
			float(dividend / divisor),
			int(quotient),
			float(remainder),
		)
