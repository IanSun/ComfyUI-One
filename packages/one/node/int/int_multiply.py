from comfy_api.latest import io
from math import prod
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	value: dict[str, float | int | None]

class OneIntMultiply(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntMultiply",
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
				io.Int.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		value = int(prod(1 if v is None else v for v in kwargs["value"].values()))

		return io.NodeOutput(value)
