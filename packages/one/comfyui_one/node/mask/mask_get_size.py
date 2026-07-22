from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class OneMaskGetSizeInputs(TypedDict):
	mask: Tensor

class OneMaskGetSize(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskGetSize",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
			],
			outputs = [
				io.Int.Output(id = "width"),
				io.Int.Output(id = "height"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskGetSizeInputs]) -> io.NodeOutput:
		shape = kwargs["mask"].shape

		return io.NodeOutput(
			shape[2],
			shape[1],
		)
