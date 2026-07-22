from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from typing import Any, TypedDict, Unpack
from ...shared.io import OneAutogrow, OneSchema

class _Inputs(TypedDict):
	input: dict[str, Any]

class OneExecutionFailover(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return OneSchema(
			node_id = "OneExecutionFailover",
			category = "One/Execution",
			inputs = [
				OneAutogrow.Input(
					id = "input",
					template = OneAutogrow.TemplatePrefix(
						input = io.AnyType.Input(id = "input"),
						prefix = "input",
						min = 0,
					),
					lazy = True,
				),
			],
			outputs = [
				io.AnyType.Output(id = "output"),
			],
			hidden = [
				io.Hidden.dynprompt,
				io.Hidden.unique_id,
			],
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		hidden = cls.hidden

		if hidden is None:
			return io.NodeOutput(None)

		dynprompt = hidden.dynprompt
		unique_id = hidden.unique_id

		node = dynprompt.get_node(unique_id)

		if node is None:
			return io.NodeOutput(None)

		inputs = node["inputs"]

		graph = GraphBuilder()

		one_execution_void = graph.node(
			class_type = "OneExecutionVoid",
			input = None,
			passthrough = False,
		)

		output = one_execution_void.out(0)
		for key in reversed(inputs):
			input = inputs[key]

			one_boolean = graph.node(
				class_type = "OneBoolean",
				value = input,
			)
			one_execution_switch = graph.node(
				class_type = "OneExecutionSwitch",
				alternative = one_boolean.out(0),
				input = output,
				input_alternative = input,
			)

			output = one_execution_switch.out(0)

		return io.NodeOutput(
			output,
			expand = graph.finalize(),
		)

	@classmethod
	def check_lazy_status(cls, **kwargs: Unpack[_Inputs]) -> list[str]:
		return []
