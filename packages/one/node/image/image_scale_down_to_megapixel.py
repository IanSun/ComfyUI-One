from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import TypedDict, Unpack
from ...shared.io import OneScaleMethod, ScaleMethod
from .image_scale_by import OneImageScaleBy

class OneImageScaleDownToMegapixelInputs(TypedDict):
	device: str
	image: Tensor
	megapixel: int
	method: ScaleMethod

class OneImageScaleDownToMegapixel(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageScaleDownToMegapixel",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
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
				io.Image.Output(id = "image"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageScaleDownToMegapixelInputs]) -> io.NodeOutput:
		image = kwargs["image"]

		shape = image.shape

		return OneImageScaleBy.execute(
			image = image,
			method = kwargs["method"],
			multiple = min(1.0, kwargs["megapixel"] * 1e6 / (shape[1] * shape[2])),
			device = kwargs["device"],
		)
