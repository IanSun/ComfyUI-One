from comfy_api.latest import io
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class _Inputs(TypedDict):
	number: dict[str, float | int | None]

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
				io.Int.Output(id = "maximum"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		maximum = max(
			(int(v) for v in kwargs["number"].values() if v is not None),
			default = None,
		)

		return io.NodeOutput(maximum)
