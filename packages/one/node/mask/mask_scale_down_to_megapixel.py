from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import TypedDict, Unpack
from ...shared.io import OneScaleMethod, ScaleMethod
from .mask_scale_by import OneMaskScaleBy

class OneMaskScaleDownToMegapixelInputs(TypedDict):
	device: str
	mask: Tensor
	megapixel: int
	method: ScaleMethod

class OneMaskScaleDownToMegapixel(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskScaleDownToMegapixel",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
				OneScaleMethod.Input(id = "method"),
				io.Float.Input(
					id = "megapixel",
					default = 1.0,
					min = 0.01,
					max = maxsize,
					step = 0.01,
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
	def execute(cls, **kwargs: Unpack[OneMaskScaleDownToMegapixelInputs]) -> io.NodeOutput:
		mask = kwargs["mask"]

		shape = mask.shape

		return OneMaskScaleBy.execute(
			mask = mask,
			method = kwargs["method"],
			multiple = min(1.0, kwargs["megapixel"] * 1e6 / (shape[1] * shape[2])),
			device = kwargs["device"],
		)
