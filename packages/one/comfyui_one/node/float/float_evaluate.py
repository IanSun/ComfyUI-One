from comfy_api.latest import io
from jsrun import Runtime, undefined
from math import isnan
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow

class OneFloatEvaluateInputs(TypedDict):
	expression: str
	input: dict[str, float | int]

class OneFloatEvaluate(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloatEvaluate",
			category = "One/Math",
			inputs = [
				OneAutogrow.Input(
					id = "input",
					template = OneAutogrow.TemplatePrefix(
						input = io.MultiType.Input(
							id = "input",
							types = [
								io.Float,
								io.Int,
							],
						),
						prefix = "input",
						min = 0,
					),
				),
				io.String.Input(
					id = "expression",
					multiline = True,
					default = "input[0]",
				),
			],
			outputs = [
				io.Float.Output(id = "output"),
			],
		)

	@classmethod
	async def execute(cls, **kwargs: Unpack[OneFloatEvaluateInputs]) -> io.NodeOutput:
		runtime = Runtime()

		try:
			runtime.bind_object(
				"input",
				{
					str(index): value
					for index, value in enumerate(kwargs["input"].values())
				},
			)
			output = await runtime.eval_async(kwargs["expression"])
			assert output is not None and output is not undefined and not isnan(output)
		finally:
			runtime.close()

		return io.NodeOutput(float(output))
