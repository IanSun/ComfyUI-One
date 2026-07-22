from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	input: tuple[str, int]
	name: str

class OneExecutionSet(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneExecutionSet",
			category = "One/Execution",
			inputs = [
				io.AnyType.Input(
					id = "input",
					lazy = True,
					raw_link = True,
				),
				io.String.Input(id = "name"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		return io.NodeOutput()

	@classmethod
	def check_lazy_status(cls, **kwargs: Unpack[_Inputs]) -> list[str]:
		return []
