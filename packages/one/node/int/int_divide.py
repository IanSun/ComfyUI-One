from comfy_api.latest import io
from sys import maxsize
from typing import TypedDict, Unpack

class OneIntDivideInputs(TypedDict):
	dividend: int
	divisor: int

class OneIntDivide(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntDivide",
			category = "One/Math",
			inputs = [
				io.Int.Input(
					id = "dividend",
					default = 0,
					min = -maxsize - 1,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "divisor",
					default = 0,
					min = -maxsize - 1,
					max = maxsize,
					step = 1,
				),
			],
			outputs = [
				io.Int.Output(id = "quotient"),
				io.Int.Output(id = "remainder"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntDivideInputs]) -> io.NodeOutput:
		return io.NodeOutput(*divmod(kwargs["dividend"], kwargs["divisor"]))
