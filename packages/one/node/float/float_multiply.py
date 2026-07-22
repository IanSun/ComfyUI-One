from comfy_api.latest import io
from math import prod
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class _Inputs(TypedDict):
	factor: dict[str, float | int | None]

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
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		product = float(prod(1 if v is None else v for v in kwargs["factor"].values()))

		return io.NodeOutput(product)
