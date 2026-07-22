from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from typing import Any, TypedDict, Unpack
from ...shared.io import OneAutogrow, OneSchema

class OneExecutionFailoverInputs(TypedDict):
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
	def execute(cls, **kwargs: Unpack[OneExecutionFailoverInputs]) -> io.NodeOutput:
		hidden = cls.hidden
		assert hidden is not None

		node = hidden.dynprompt.get_node(hidden.unique_id)
		assert node is not None

		inputs = node["inputs"]

		graph = GraphBuilder()

		output = None
		for input in reversed(inputs.values()):
			one_any_convert_to_boolean = graph.node(
				class_type = "OneAnyConvertToBoolean",
				value = input,
			)
			one_execution_switch = graph.node(
				class_type = "OneExecutionSwitch",
				input = output,
				input_alternative = input,
				alternative = one_any_convert_to_boolean.out(0),
			)

			output = one_execution_switch.out(0)

		return io.NodeOutput(
			output,
			expand = graph.finalize(),
		)

	@classmethod
	def check_lazy_status(cls, **kwargs: Unpack[OneExecutionFailoverInputs]) -> list[str]:
		return []
