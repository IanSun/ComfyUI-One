from comfy_api.latest import io
from decimal import Decimal, ROUND_HALF_UP
from sys import maxsize
from typing import TypedDict, Unpack

class OneFloatRoundInputs(TypedDict):
	number: float
	precision: int

class OneFloatRound(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatRound",
			category = "One/Math",
			inputs = [
				io.Float.Input(
					id = "number",
					default = 0.0,
					min = -maxsize - 1,
					max = maxsize,
					step = 0.01,
				),
				io.Int.Input(
					id = "precision",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
			],
			outputs = [
				io.Float.Output(id = "number"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatRoundInputs]) -> io.NodeOutput:
		return io.NodeOutput(
			float(
				Decimal(str(kwargs["number"]))
					.quantize(
						exp = Decimal(1).scaleb(-kwargs["precision"]),
						rounding = ROUND_HALF_UP,
					)
			)
		)
