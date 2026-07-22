from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class OneImageGetResolutionInputs(TypedDict):
	image: Tensor

class OneImageGetResolution(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetResolution",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
			],
			outputs = [
				io.Int.Output(id = "resolution"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageGetResolutionInputs]) -> io.NodeOutput:
		shape = kwargs["image"].shape

		return io.NodeOutput(shape[1] * shape[2])
