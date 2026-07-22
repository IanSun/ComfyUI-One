from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	mask: Tensor

class OneMaskGetHeight(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskGetHeight",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
			],
			outputs = [
				io.Int.Output(id = "height"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		height = kwargs["mask"].shape[1]

		return io.NodeOutput(height)
