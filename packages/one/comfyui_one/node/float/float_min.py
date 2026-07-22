from comfy_api.latest import io
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class OneFloatMinInputs(TypedDict):
	number: dict[str, float | int]

class OneFloatMin(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatMin",
			category = "One/Math",
			inputs = [
				OneAutogrow.Input(
					id = "number",
					template = OneAutogrow.TemplatePrefix(
						input = io.MultiType.Input(
							id = "number",
							types = [
								io.Float,
								io.Int,
							],
						),
						prefix = "number",
						min = 0,
					),
				),
			],
			outputs = [
				io.Float.Output(id = "minimum"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatMinInputs]) -> io.NodeOutput:
		return io.NodeOutput(float(min(kwargs["number"].values())))
