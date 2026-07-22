from comfy_api.latest import io
from decimal import Decimal
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class OneFloatAddInputs(TypedDict):
	addend: dict[str, float | int]

class OneFloatAdd(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatAdd",
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
				io.Float.Output(id = "sum"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneFloatAddInputs]) -> io.NodeOutput:
		return io.NodeOutput(float(sum(Decimal(str(value)) for value in kwargs["addend"].values())))
