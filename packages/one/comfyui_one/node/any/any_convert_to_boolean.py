from comfy_api.latest import io
from typing import Any, TypedDict, Unpack

class OneAnyConvertToBooleanInputs(TypedDict):
	value: Any

class OneAnyConvertToBoolean(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneAnyConvertToBoolean",
			category = "One/Primitive",
			inputs = [
				io.AnyType.Input(id = "value"),
			],
			outputs = [
				io.Boolean.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneAnyConvertToBooleanInputs]) -> io.NodeOutput:
		try:
			return io.NodeOutput(bool(kwargs["value"]))
		except RuntimeError:
			return io.NodeOutput(True)
