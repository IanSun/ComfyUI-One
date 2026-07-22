from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import TypedDict, Unpack, assert_never
from ...shared.io import Alignment, OneAlignment
from .image_crop import OneImageCrop

class OneImageCropByAlignmentInputs(TypedDict):
	alignment: Alignment
	device: str
	height: int
	image: Tensor
	width: int

class OneImageCropByAlignment(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageCropByAlignment",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
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
				OneAlignment.Input(id = "alignment"),
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
	def execute(cls, **kwargs: Unpack[OneImageCropByAlignmentInputs]) -> io.NodeOutput:
		alignment = kwargs["alignment"]
		height = kwargs["height"]
		image = kwargs["image"]
		width = kwargs["width"]

		match alignment:
			case Alignment.BottomLeft | Alignment.Left | Alignment.TopLeft:
				x = 0

			case Alignment.BottomRight | Alignment.Right | Alignment.TopRight:
				x = max(0, image.shape[2] - width)

			case Alignment.Bottom | Alignment.Center | Alignment.Top:
				x = max(0, image.shape[2] - width) // 2

			case _:
				assert_never(alignment)

		match alignment:
			case Alignment.Top | Alignment.TopLeft | Alignment.TopRight:
				y = 0

			case Alignment.Bottom | Alignment.BottomLeft | Alignment.BottomRight:
				y = max(0, image.shape[1] - height)

			case Alignment.Center | Alignment.Left | Alignment.Right:
				y = max(0, image.shape[1] - height) // 2

			case _:
				assert_never(alignment)

		return OneImageCrop.execute(
			image = image,
			x = x,
			y = y,
			width = width,
			height = height,
			device = kwargs["device"],
		)
