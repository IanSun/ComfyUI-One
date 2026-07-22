from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import TypedDict, Unpack
from ...shared.io import OneScaleMethod, ScaleMethod
from .mask_scale_by import OneMaskScaleBy

class OneMaskScaleDownByLongerEdgeInputs(TypedDict):
	device: str
	mask: Tensor
	method: ScaleMethod
	size: int

class OneMaskScaleDownByLongerEdge(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskScaleDownByLongerEdge",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
				OneScaleMethod.Input(
					id = "method",
					default = ScaleMethod.Area,
				),
				io.Int.Input(
					id = "size",
					default = 1024,
					min = 1,
					max = maxsize,
					step = 1,
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					default = "default",
					advanced = True,
				),
			],
			outputs = [
				io.Mask.Output(id = "mask"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskScaleDownByLongerEdgeInputs]) -> io.NodeOutput:
		mask = kwargs["mask"]

		return OneMaskScaleBy.execute(
			mask = mask,
			method = kwargs["method"],
			multiple = min(1.0, kwargs["size"] / max(mask.shape[1:3])),
			device = kwargs["device"],
		)
