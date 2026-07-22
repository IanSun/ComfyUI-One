from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import TypedDict, Unpack

class OneMaskCropInputs(TypedDict):
	device: str
	height: int
	mask: Tensor
	width: int
	x: int
	y: int

class OneMaskCrop(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskCrop",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
				io.Int.Input(
					id = "x",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "y",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "width",
					default = 1024,
					min = 1,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "height",
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
	def execute(cls, **kwargs: Unpack[OneMaskCropInputs]) -> io.NodeOutput:
		mask = kwargs["mask"]

		shape = mask.shape

		mask_height = shape[1]
		y1 = kwargs["y"]

		if mask_height <= y1:
			return io.NodeOutput(None)

		mask_width = shape[2]
		x1 = kwargs["x"]

		if mask_width <= x1:
			return io.NodeOutput(None)

		x2 = min(mask_width, x1 + kwargs["width"])
		y2 = min(mask_height, y1 + kwargs["height"])

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			mask = mask.to(device = device)

		if (0, 0, mask_width, mask_height) != (x1, y1, x2, y2):
			mask = mask[:, y1:y2, x1:x2]

		return io.NodeOutput(mask)
