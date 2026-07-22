from comfy_api.latest import io
from os import urandom
from typing import Any, TypedDict, Unpack

class _Inputs(TypedDict):
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
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		hidden = cls.hidden

		if hidden is None:
			return io.NodeOutput(None)

		dynprompt = hidden.dynprompt
		unique_id = hidden.unique_id

		name = kwargs["name"]

		output = None
		for id in dynprompt.all_node_ids():
			if unique_id == id:
				continue

			node = dynprompt.get_node(id)

			if node is None or "OneExecutionSet" != node["class_type"]:
				continue

			inputs = node["inputs"]

			if name == inputs["name"]:
				output = inputs["input"]
				break

		return io.NodeOutput(
			output,
			expand = {},
		)

	@classmethod
	def fingerprint_inputs(cls, **kwargs: Any) -> Any:
		return urandom(16).hex()
