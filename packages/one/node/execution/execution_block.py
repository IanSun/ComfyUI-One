from comfy_api.latest import io
from comfy_execution.graph import ExecutionBlocker
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	input: tuple[str, int]
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
					raw_link = True,
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
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		if kwargs["passthrough"]:
			output = kwargs["input"]

			return io.NodeOutput(
				output,
				expand = {},
			)

		return io.NodeOutput(ExecutionBlocker(None))

	@classmethod
	def check_lazy_status(cls, **kwargs: Unpack[_Inputs]) -> list[str]:
		return []
