from comfy_api.latest import io
from typing import TypedDict, Unpack

class OneIntAlignDownToMultipleInputs(TypedDict):
	base: int
	number: int

class OneIntAlignDownToMultiple(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntAlignDownToMultiple",
			category = "One/Math",
			inputs = [
				io.Int.Input(
					id = "number",
					default = 0,
					min = 0,
				),
				io.Int.Input(
					id = "base",
					default = 1,
					min = 1,
				),
			],
			outputs = [
				io.Int.Output(id = "number"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntAlignDownToMultipleInputs]) -> io.NodeOutput:
		base = kwargs["base"]

		return io.NodeOutput(kwargs["number"] // base * base)
