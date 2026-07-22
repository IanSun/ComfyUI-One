from comfy_api.latest import io
from math import prod
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class OneIntMultiplyInputs(TypedDict):
	factor: dict[str, int]

class OneIntMultiply(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntMultiply",
			category = "One/Math",
			inputs = [
				OneAutogrow.Input(
					id = "factor",
					template = OneAutogrow.TemplatePrefix(
						input = io.Int.Input(id = "factor"),
						prefix = "factor",
						min = 0,
					),
				),
			],
			outputs = [
				io.Int.Output(id = "product"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntMultiplyInputs]) -> io.NodeOutput:
		return io.NodeOutput(prod(kwargs["factor"].values()))
