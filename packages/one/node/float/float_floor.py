from comfy_api.latest import io
from decimal import Decimal
from math import floor
from sys import maxsize
from typing import TypedDict, Unpack

class OneFloatFloorInputs(TypedDict):
	number: float
	precision: int

class OneFloatFloor(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatFloor",
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
	def execute(cls, **kwargs: Unpack[OneFloatFloorInputs]) -> io.NodeOutput:
		precision = kwargs["precision"]

		return io.NodeOutput(float(Decimal(floor(Decimal(str(kwargs["number"])).shift(precision))).shift(-precision)))
