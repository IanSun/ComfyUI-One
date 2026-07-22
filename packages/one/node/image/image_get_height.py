from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	image: Tensor

class OneImageGetHeight(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetHeight",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
			],
			outputs = [
				io.Int.Output(id = "height"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		height = kwargs["image"].shape[1]

		return io.NodeOutput(height)
