from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	base: float | int
	exponent: float | int

class OneIntExponentiate(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneIntExponentiate",
			category = "One/Math",
			inputs = [
				io.MultiType.Input(
					id = "base",
					types = [
						io.Float,
						io.Int,
					],
				),
				io.MultiType.Input(
					id = "exponent",
					types = [
						io.Float,
						io.Int,
					],
				),
			],
			outputs = [
				io.Int.Output(id = "power"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		power = int(kwargs["base"] ** kwargs["exponent"])

		return io.NodeOutput(power)
