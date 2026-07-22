from comfy_api.latest import io
from sys import maxsize
from typing import TypedDict, Unpack

class OneIntExponentiateInputs(TypedDict):
	base: int
	exponent: int

class OneIntExponentiate(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntExponentiate",
			category = "One/Math",
			inputs = [
				io.Int.Input(
					id = "base",
					default = 0,
					min = -maxsize - 1,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "exponent",
					default = 0,
					min = -maxsize - 1,
					max = maxsize,
					step = 1,
				),
			],
			outputs = [
				io.Int.Output(id = "power"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneIntExponentiateInputs]) -> io.NodeOutput:
		return io.NodeOutput(kwargs["base"] ** kwargs["exponent"])
