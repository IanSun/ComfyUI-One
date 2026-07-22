from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class OneMaskGetShorterEdgeInputs(TypedDict):
	mask: Tensor

class OneMaskGetShorterEdge(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskGetShorterEdge",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
			],
			outputs = [
				io.Int.Output(id = "edge"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskGetShorterEdgeInputs]) -> io.NodeOutput:
		return io.NodeOutput(min(kwargs["mask"].shape[1:3]))
