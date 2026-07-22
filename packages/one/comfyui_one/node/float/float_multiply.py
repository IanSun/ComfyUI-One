from comfy_api.latest import io
from decimal import Decimal
from math import prod
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class OneFloatMultiplyInputs(TypedDict):
	factor: dict[str, float | int]

class OneFloatMultiply(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatMultiply",
			category = "One/Math",
			inputs = [
				OneAutogrow.Input(
					id = "factor",
					template = OneAutogrow.TemplatePrefix(
						input = io.MultiType.Input(
							id = "factor",
							types = [
								io.Float,
								io.Int,
							],
						),
						prefix = "factor",
						min = 0,
					),
				),
			],
			outputs = [
				io.Float.Output(id = "product"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatMultiplyInputs]) -> io.NodeOutput:
		return io.NodeOutput(float(prod(Decimal(str(value)) for value in kwargs["factor"].values())))
