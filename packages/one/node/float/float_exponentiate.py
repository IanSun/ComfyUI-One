from comfy_api.latest import io
from decimal import Decimal
from typing import TypedDict, Unpack

class OneFloatExponentiateInputs(TypedDict):
	base: float | int
	exponent: float | int

class OneFloatExponentiate(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatExponentiate",
			category = "One/Math",
			inputs = [
				io.MultiType.Input(
					id = "base",
					types = [
						io.Float,
						io.Int,
					],
				),
				io.MultiType.Input(
					id = "exponent",
					types = [
						io.Float,
						io.Int,
					],
				),
			],
			outputs = [
				io.Float.Output(id = "power"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatExponentiateInputs]) -> io.NodeOutput:
		return io.NodeOutput(float(Decimal(str(kwargs["base"])) ** Decimal(str(kwargs["exponent"]))))
