from comfy_api.latest import io
from comfy_execution.graph import ExecutionBlocker
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	input: io.AnyType.Type
	passthrough: io.Boolean.Type

class OneExecutionBlock(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		template = io.MatchType.Template("input")

		return io.Schema(
			node_id = "OneExecutionBlock",
			display_name = "执行阻止",
			category = "One/实用工具/逻辑",
			inputs = [
				io.MatchType.Input(
					id = "input",
					template = template,
					display_name = "输入",
					lazy = True,
				),
				io.Boolean.Input(
					id = "passthrough",
					display_name = "通过",
					default = True,
				),
			],
			outputs = [
				io.MatchType.Output(
					template = template,
					id = "output",
					display_name = "输出",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		if kwargs["passthrough"]:
			return io.NodeOutput(kwargs["input"])

		return io.NodeOutput(ExecutionBlocker(None))

	@classmethod
	def check_lazy_status(cls, **kwargs: Unpack[_Inputs]) -> list[str]:
		if kwargs["passthrough"]:
			return ["input"]

		return []
