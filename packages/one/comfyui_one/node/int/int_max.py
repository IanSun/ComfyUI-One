from comfy_api.latest import io
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class OneIntMaxInputs(TypedDict):
	number: dict[str, int]

class OneIntMax(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntMax",
			category = "One/Math",
			inputs = [
				OneAutogrow.Input(
					id = "number",
					template = OneAutogrow.TemplatePrefix(
						input = io.Int.Input(id = "number"),
						prefix = "number",
						min = 0,
					),
				),
			],
			outputs = [
				io.Int.Output(id = "maximum"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntMaxInputs]) -> io.NodeOutput:
		return io.NodeOutput(max(kwargs["number"].values()))
