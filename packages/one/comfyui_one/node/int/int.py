from comfy_api.latest import io
from sys import maxsize
from typing import TypedDict, Unpack

class OneIntInputs(TypedDict):
	value: int

class OneInt(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneInt",
			category = "One/Primitive",
			inputs = [
				io.Int.Input(
					id = "value",
					default = 0,
					min = -maxsize - 1,
					max = maxsize,
					step = 1,
					socketless = True,
				),
			],
			outputs = [
				io.Int.Output(id = "value"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntInputs]) -> io.NodeOutput:
		return io.NodeOutput(kwargs["value"])
