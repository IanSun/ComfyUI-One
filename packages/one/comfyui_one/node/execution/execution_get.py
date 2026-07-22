from comfy_api.latest import io
from comfy_execution.graph import ExecutionBlocker
from os import urandom
from typing import Any, TypedDict, Unpack

class OneExecutionGetInputs(TypedDict):
	name: str

class OneExecutionGet(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneExecutionGet",
			category = "One/Execution",
			inputs = [
				io.String.Input(id = "name"),
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
	def execute(cls, **kwargs: Unpack[OneExecutionGetInputs]) -> io.NodeOutput:
		hidden = cls.hidden
		assert hidden is not None

		dynprompt = hidden.dynprompt
		unique_id = hidden.unique_id

		name = kwargs["name"]

		for id in dynprompt.all_node_ids():
			if unique_id == id:
				continue

			node = dynprompt.get_node(id)
			assert node is not None

			if "OneExecutionSet" != node["class_type"]:
				continue

			inputs = node["inputs"]

			if name == inputs["name"]:
				return io.NodeOutput(
					inputs["input"],
					expand = {},
				)

		return io.NodeOutput(ExecutionBlocker(None))

	@classmethod
	def fingerprint_inputs(cls, **kwargs: Unpack[OneExecutionGetInputs]) -> Any:
		return urandom(16).hex()
