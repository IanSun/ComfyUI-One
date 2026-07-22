from comfy_api.latest import io
from comfy_execution.graph import ExecutionBlocker
from typing import Any, Unpack, cast
from .typing import OneListSelectByIndexInputs

class OneListSelectByIndex(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneListSelectByIndex",
			display_name = "列表选择（序号）",
			category = "One/实用工具",
			inputs = [
				io.AnyType.Input(
					id = "input",
					display_name = "输入",
				),
				io.Int.Input(
					id = "index",
					display_name = "序号",
					default = 0,
					min = 0,
				),
			],
			outputs = [
				io.AnyType.Output(
					id = "output",
					display_name = "输出",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneListSelectByIndexInputs]) -> io.NodeOutput:
		index = kwargs.get("index")
		input = kwargs.get("input")

		if not isinstance(input, list):
			return io.NodeOutput(ExecutionBlocker("输入不是列表"))

		if len(cast(list[Any], input)) <= index:
			return io.NodeOutput(ExecutionBlocker("序号超过列表长度"))

		output = cast(list[Any], input)[index]

		return io.NodeOutput(output)
