from comfy_api.latest import io
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class _Inputs(TypedDict):
	addend: dict[str, float | int | None]

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
						input = io.MultiType.Input(
							id = "addend",
							types = [
								io.Float,
								io.Int,
							],
						),
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
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		output = int(sum(0 if v is None else v for v in kwargs["addend"].values()))

		return io.NodeOutput(output)
