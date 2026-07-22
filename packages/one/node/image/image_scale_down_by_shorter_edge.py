from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import TypedDict, Unpack
from ...shared.io import OneScaleMethod, ScaleMethod
from .image_scale_by import OneImageScaleBy

class OneImageScaleDownByShorterEdgeInputs(TypedDict):
	device: str
	image: Tensor
	method: ScaleMethod
	size: int

class OneImageScaleDownByShorterEdge(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageScaleDownByShorterEdge",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
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
				io.Image.Output(id = "image"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageScaleDownByShorterEdgeInputs]) -> io.NodeOutput:
		image = kwargs["image"]

		return OneImageScaleBy.execute(
			image = image,
			method = kwargs["method"],
			multiple = min(1.0, kwargs["size"] / min(image.shape[1:3])),
			device = kwargs["device"],
		)
