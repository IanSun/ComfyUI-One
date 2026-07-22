from comfy_api.latest import io
from comfy_execution.graph import ExecutionBlocker
from typing import Any, TypedDict, Unpack

class OneExecutionBlockInputs(TypedDict):
	input: Any
	passthrough: bool

class OneExecutionBlock(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		template = io.MatchType.Template("input")

		return io.Schema(
			node_id = "OneExecutionBlock",
			category = "One/Execution",
			inputs = [
				io.MatchType.Input(
					id = "input",
					template = template,
					lazy = True,
				),
				io.Boolean.Input(
					id = "passthrough",
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
	def execute(cls, **kwargs: Unpack[OneExecutionBlockInputs]) -> io.NodeOutput:
		if kwargs["passthrough"]:
			return io.NodeOutput(kwargs["input"])

		return io.NodeOutput(ExecutionBlocker(None))

	@classmethod
	def check_lazy_status(cls, **kwargs: Unpack[OneExecutionBlockInputs]) -> list[str]:
		if kwargs["passthrough"]:
			return ["input"]

		return []
