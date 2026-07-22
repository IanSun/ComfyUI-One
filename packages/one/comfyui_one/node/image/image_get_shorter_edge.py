from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class OneImageGetShorterEdgeInputs(TypedDict):
	image: Tensor

class OneImageGetShorterEdge(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetShorterEdge",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
			],
			outputs = [
				io.Int.Output(id = "edge"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageGetShorterEdgeInputs]) -> io.NodeOutput:
		return io.NodeOutput(min(kwargs["image"].shape[1:3]))
