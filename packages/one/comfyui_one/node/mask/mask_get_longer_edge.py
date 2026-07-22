from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class OneMaskGetLongerEdgeInputs(TypedDict):
	mask: Tensor

class OneMaskGetLongerEdge(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskGetLongerEdge",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
			],
			outputs = [
				io.Int.Output(id = "edge"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskGetLongerEdgeInputs]) -> io.NodeOutput:
		return io.NodeOutput(max(kwargs["mask"].shape[1:3]))
