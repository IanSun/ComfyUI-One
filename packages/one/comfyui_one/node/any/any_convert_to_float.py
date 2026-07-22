from comfy_api.latest import io
from typing import Any, TypedDict, Unpack
from .any_convert_to_boolean import OneAnyConvertToBoolean

class OneAnyConvertToFloatInputs(TypedDict):
	value: Any

class OneAnyConvertToFloat(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneAnyConvertToFloat",
			category = "One/Primitive",
			inputs = [
				io.AnyType.Input(id = "value"),
			],
			outputs = [
				io.Float.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneAnyConvertToFloatInputs]) -> io.NodeOutput:
		value = kwargs["value"]

		try:
			return io.NodeOutput(float(value))
		except (TypeError, ValueError):
			return io.NodeOutput(float(OneAnyConvertToBoolean.execute(value = value)[0]))
