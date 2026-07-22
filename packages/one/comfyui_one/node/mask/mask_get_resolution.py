from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class OneMaskGetResolutionInputs(TypedDict):
	mask: Tensor

class OneMaskGetResolution(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskGetResolution",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
			],
			outputs = [
				io.Int.Output(id = "resolution"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskGetResolutionInputs]) -> io.NodeOutput:
		shape = kwargs["mask"].shape

		return io.NodeOutput(shape[1] * shape[2])
