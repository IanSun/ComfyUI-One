from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import TypedDict, Unpack

class OneImageCropInputs(TypedDict):
	device: str
	height: int
	image: Tensor
	width: int
	x: int
	y: int

class OneImageCrop(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageCrop",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
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
				io.Image.Output(id = "image"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageCropInputs]) -> io.NodeOutput:
		image = kwargs["image"]

		shape = image.shape

		image_height = shape[1]
		y1 = kwargs["y"]

		if image_height <= y1:
			return io.NodeOutput(None)

		image_width = shape[2]
		x1 = kwargs["x"]

		if image_width <= x1:
			return io.NodeOutput(None)

		x2 = min(image_width, x1 + kwargs["width"])
		y2 = min(image_height, y1 + kwargs["height"])

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			image = image.to(device = device)

		if (0, 0, image_width, image_height) != (x1, y1, x2, y2):
			image = image[:, y1:y2, x1:x2, :]

		return io.NodeOutput(image)
