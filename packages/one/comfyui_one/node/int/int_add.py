from comfy_api.latest import io
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class OneIntAddInputs(TypedDict):
	addend: dict[str, int]

class OneIntAdd(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntAdd",
			category = "One/Math",
			inputs = [
				OneAutogrow.Input(
					id = "addend",
					template = OneAutogrow.TemplatePrefix(
						input = io.Int.Input(id = "addend"),
						prefix = "addend",
						min = 0,
					),
				),
			],
			outputs = [
				io.Int.Output(id = "sum"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntAddInputs]) -> io.NodeOutput:
		return io.NodeOutput(sum(kwargs["addend"].values()))
