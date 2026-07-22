from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	alternative: bool
	input: tuple[str, int]
	input_alternative: tuple[str, int]

class OneExecutionSwitch(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneExecutionSwitch",
			category = "One/Execution",
			inputs = [
				io.AnyType.Input(
					id = "input",
					lazy = True,
					raw_link = True,
				),
				io.AnyType.Input(
					id = "input_alternative",
					lazy = True,
					raw_link = True,
				),
				io.Boolean.Input(
					id = "alternative",
					default = False,
				),
			],
			outputs = [
				io.AnyType.Output(id = "output"),
			],
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		graph = GraphBuilder()

		one_execution_select = graph.node(
			class_type = "OneExecutionSelect",
			id = None,
			**{
				"index": int(kwargs["alternative"]),
				"input.input0": kwargs["input"],
				"input.input1": kwargs["input_alternative"],
			},
		)

		output = one_execution_select.out(0)

		return io.NodeOutput(
			output,
			expand = graph.finalize(),
		)

	@classmethod
	def check_lazy_status(cls, **kwargs: Unpack[_Inputs]) -> list[str]:
		return []
