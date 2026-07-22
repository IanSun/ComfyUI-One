from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import NotRequired, TypedDict, Unpack, assert_never
from ...shared.io import Alignment, OneAlignment
from .image_pad import OneImagePad

class OneImagePadToMultipleInputs(TypedDict):
	alignment: Alignment
	color: str
	device: str
	image: Tensor
	mask: NotRequired[Tensor]
	multiple: int

class OneImagePadToMultiple(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImagePadToMultiple",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
				io.Mask.Input(
					id = "mask",
					optional = True,
				),
				io.Int.Input(
					id = "multiple",
					default = 8,
					min = 1,
					max = maxsize,
					step = 1,
				),
				OneAlignment.Input(
					id = "alignment",
					default = Alignment.TopLeft,
				),
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
	def execute(cls, **kwargs: Unpack[OneImagePadToMultipleInputs]) -> io.NodeOutput:
		alignment = kwargs["alignment"]
		image = kwargs["image"]
		multiple = kwargs["multiple"]

		match alignment:
			case Alignment.BottomLeft | Alignment.Left | Alignment.TopLeft:
				left = 0
				right = multiple - image.shape[2] % multiple

			case Alignment.BottomRight | Alignment.Right | Alignment.TopRight:
				left = multiple - image.shape[2] % multiple
				right = 0

			case Alignment.Bottom | Alignment.Center | Alignment.Top:
				dx = multiple - image.shape[2] % multiple
				left = dx // 2
				right = dx - left

			case _:
				assert_never(alignment)

		match alignment:
			case Alignment.Top | Alignment.TopLeft | Alignment.TopRight:
				top = 0
				bottom = multiple - image.shape[1] % multiple

			case Alignment.Bottom | Alignment.BottomLeft | Alignment.BottomRight:
				top = multiple - image.shape[1] % multiple
				bottom = 0

			case Alignment.Center | Alignment.Left | Alignment.Right:
				dy = multiple - image.shape[1] % multiple
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
