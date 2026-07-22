from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	image: Tensor

class OneImageGetWidth(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetWidth",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
			],
			outputs = [
				io.Int.Output(id = "width"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		width = kwargs["image"].shape[2]

		return io.NodeOutput(width)
