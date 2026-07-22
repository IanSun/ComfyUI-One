from comfy_api.latest import io
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class OneFloatMaxInputs(TypedDict):
	number: dict[str, float | int]

class OneFloatMax(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatMax",
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
				io.Float.Output(id = "maximum"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatMaxInputs]) -> io.NodeOutput:
		return io.NodeOutput(float(max(kwargs["number"].values())))
