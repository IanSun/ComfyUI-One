from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import NotRequired, TypedDict, Unpack, assert_never
from ...shared.io import Alignment, OneAlignment
from .image_pad import OneImagePad

class OneImagePadToSizeInputs(TypedDict):
	alignment: Alignment
	color: str
	device: str
	height: int
	image: Tensor
	mask: NotRequired[Tensor]
	width: int

class OneImagePadToSize(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImagePadToSize",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
				io.Mask.Input(
					id = "mask",
					optional = True,
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
				OneAlignment.Input(id = "alignment"),
				io.Color.Input(
					id = "color",
					default = "#FFFFFF",
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
	def execute(cls, **kwargs: Unpack[OneImagePadToSizeInputs]) -> io.NodeOutput:
		alignment = kwargs["alignment"]
		height = kwargs["height"]
		image = kwargs["image"]
		width = kwargs["width"]

		match alignment:
			case Alignment.BottomLeft | Alignment.Left | Alignment.TopLeft:
				left = 0
				right = max(0, width - image.shape[2])

			case Alignment.BottomRight | Alignment.Right | Alignment.TopRight:
				left = max(0, width - image.shape[2])
				right = 0

			case Alignment.Bottom | Alignment.Center | Alignment.Top:
				dx = max(0, width - image.shape[2])
				left = dx // 2
				right = dx - left

			case _:
				assert_never(alignment)

		match alignment:
			case Alignment.Top | Alignment.TopLeft | Alignment.TopRight:
				top = 0
				bottom = max(0, height - image.shape[1])

			case Alignment.Bottom | Alignment.BottomLeft | Alignment.BottomRight:
				top = max(0, height - image.shape[1])
				bottom = 0

			case Alignment.Center | Alignment.Left | Alignment.Right:
				dy = max(0, height - image.shape[1])
				top = dy // 2
				bottom = dy - top

			case _:
				assert_never(alignment)

		return OneImagePad.execute(
			image = image,
			**({
				"mask": kwargs["mask"],
			} if "mask" in kwargs else {}),
			top = top,
			right = right,
			bottom = bottom,
			left = left,
			color = kwargs["color"],
			device = kwargs["device"],
		)
