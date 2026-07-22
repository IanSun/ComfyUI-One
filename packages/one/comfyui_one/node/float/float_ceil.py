from comfy_api.latest import io
from decimal import Decimal
from math import ceil
from typing import TypedDict, Unpack

class OneFloatCeilInputs(TypedDict):
	number: float
	precision: int

class OneFloatCeil(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatCeil",
			category = "One/Math",
			inputs = [
				io.Float.Input(
					id = "number",
					default = 0.0,
				),
				io.Int.Input(
					id = "precision",
					default = 0,
					min = 0,
				),
			],
			outputs = [
				io.Float.Output(id = "number"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatCeilInputs]) -> io.NodeOutput:
		precision = kwargs["precision"]

		return io.NodeOutput(float(Decimal(ceil(Decimal(str(kwargs["number"])).shift(precision))).shift(-precision)))
