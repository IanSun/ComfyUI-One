from comfy_api.latest import io
from typing import Any, TypedDict, Unpack

class OneExecutionSwitchInputs(TypedDict):
	alternative: bool
	input: Any
	input_alternative: Any

class OneExecutionSwitch(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		template = io.MatchType.Template("input")

		return io.Schema(
			node_id = "OneExecutionSwitch",
			category = "One/Execution",
			inputs = [
				io.MatchType.Input(
					id = "input",
					template = template,
					lazy = True,
				),
				io.MatchType.Input(
					id = "input_alternative",
					template = template,
					lazy = True,
				),
				io.Boolean.Input(
					id = "alternative",
					default = False,
				),
			],
			outputs = [
				io.MatchType.Output(
					template = template,
					id = "output",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneExecutionSwitchInputs]) -> io.NodeOutput:
		return io.NodeOutput(kwargs["input_alternative"] if kwargs["alternative"] else kwargs["input"])

	@classmethod
	def check_lazy_status(cls, **kwargs: Unpack[OneExecutionSwitchInputs]) -> list[str]:
		return ["alternative"] if kwargs["input_alternative"] else ["input"]
