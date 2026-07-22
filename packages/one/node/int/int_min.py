from comfy_api.latest import io
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class OneIntMinInputs(TypedDict):
	number: dict[str, int]

class OneIntMin(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntMin",
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
				io.Int.Output(id = "minimum"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntMinInputs]) -> io.NodeOutput:
		return io.NodeOutput(min(kwargs["number"].values()))
