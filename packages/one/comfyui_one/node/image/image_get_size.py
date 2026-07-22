from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class OneImageGetSizeInputs(TypedDict):
	image: Tensor

class OneImageGetSize(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetSize",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
			],
			outputs = [
				io.Int.Output(id = "width"),
				io.Int.Output(id = "height"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageGetSizeInputs]) -> io.NodeOutput:
		shape = kwargs["image"].shape

		return io.NodeOutput(
			shape[2],
			shape[1],
		)
