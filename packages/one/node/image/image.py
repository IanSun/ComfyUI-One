from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import float32, tensor
from typing import TypedDict, Unpack
from ..mask.mask import OneMask

class OneImageInputs(TypedDict):
	batch: int
	color: str
	device: str
	height: int
	width: int

class OneImage(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImage",
			category = "One/Image",
			inputs = [
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
				io.Color.Input(
					id = "color",
					default = "#FFFFFF",
				),
				io.Int.Input(
					id = "batch",
					default = 1,
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
				io.Mask.Output(id = "mask"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageInputs]) -> io.NodeOutput:
		color = kwargs["color"].lstrip("#")

		try:
			red, green, blue, *color_ = (value / 255.0 for value in bytes.fromhex(color))
			alpha = color_[0] if color_ else 1.0
		except ValueError:
			red, green, blue, alpha = 1.0, 1.0, 1.0, 1.0

		device = kwargs["device"]

		image = tensor(
			data = (red, green, blue),
			dtype = float32,
			device = resolve_gpu_device_option(device),
		)

		batch = kwargs["batch"]
		height = kwargs["height"]
		width = kwargs["width"]

		image = image.expand(batch, height, width, 3)

		mask = OneMask.execute(
			width = width,
			height = height,
			value = 1.0 - alpha,
			batch = batch,
			device = device,
		)[0]

		return io.NodeOutput(
			image,
			mask,
		)
