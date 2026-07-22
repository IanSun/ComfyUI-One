from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	mask: Tensor

class OneMaskGetWidth(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskGetWidth",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
			],
			outputs = [
				io.Int.Output(id = "width"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		width = kwargs["mask"].shape[2]

		return io.NodeOutput(width)
