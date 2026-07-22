from comfy_api.latest import io
from typing import Any, TypedDict, Unpack
from .any_convert_to_boolean import OneAnyConvertToBoolean

class OneAnyConvertToIntInputs(TypedDict):
	value: Any

class OneAnyConvertToInt(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneAnyConvertToInt",
			category = "One/Primitive",
			inputs = [
				io.AnyType.Input(id = "value"),
			],
			outputs = [
				io.Int.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneAnyConvertToIntInputs]) -> io.NodeOutput:
		value = kwargs["value"]

		try:
			return io.NodeOutput(int(value))
		except (TypeError, ValueError):
			return io.NodeOutput(int(OneAnyConvertToBoolean.execute(value = value)[0]))
