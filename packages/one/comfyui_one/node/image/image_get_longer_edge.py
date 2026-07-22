from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class OneImageGetLongerEdgeInputs(TypedDict):
	image: Tensor

class OneImageGetLongerEdge(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetLongerEdge",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
			],
			outputs = [
				io.Int.Output(id = "edge"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageGetLongerEdgeInputs]) -> io.NodeOutput:
		return io.NodeOutput(max(kwargs["image"].shape[1:3]))
