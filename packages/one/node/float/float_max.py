from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	value: dict[str, float | int | None]

class OneFloatMax(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatMax",
			category = "One/Math",
			inputs = [
				io.Autogrow.Input(
					id = "value",
					template = io.Autogrow.TemplatePrefix(
						input = io.MultiType.Input(
							id = "value",
							types = [
								io.Float,
								io.Int,
							],
						),
						prefix = "value",
						min = 0,
						max = 10,
					),
				),
			],
			outputs = [
				io.Float.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		value = max((float(v) for v in kwargs["value"].values() if v is not None), default = None)

		return io.NodeOutput(value)
