from comfy_api.latest import io
from sys import maxsize
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	value: float

class OneFloat(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneFloat",
			category = "One/Primitive",
			inputs = [
				io.Float.Input(
					id = "value",
					default = 0,
					min = -maxsize,
					max = maxsize,
					step = 0.01,
					socketless = True,
				),
			],
			outputs = [
				io.Int.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		value = kwargs["value"]

		return io.NodeOutput(value)
