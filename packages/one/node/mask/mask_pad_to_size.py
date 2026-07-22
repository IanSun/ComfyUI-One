from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import TypedDict, Unpack, assert_never
from ...shared.io import Alignment, OneAlignment
from .mask_pad import OneMaskPad

class OneMaskPadToSizeInputs(TypedDict):
	alignment: Alignment
	device: str
	height: int
	mask: Tensor
	value: float
	width: int

class OneMaskPadToSize(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskPadToSize",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
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
				io.Float.Input(
					id = "value",
					default = 0.0,
					min = 0.0,
					max = 1.0,
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
	def execute(cls, **kwargs: Unpack[OneMaskPadToSizeInputs]) -> io.NodeOutput:
		alignment = kwargs["alignment"]
		height = kwargs["height"]
		mask = kwargs["mask"]
		width = kwargs["width"]

		match alignment:
			case Alignment.BottomLeft | Alignment.Left | Alignment.TopLeft:
				left = 0
				right = max(0, width - mask.shape[2])

			case Alignment.BottomRight | Alignment.Right | Alignment.TopRight:
				left = max(0, width - mask.shape[2])
				right = 0

			case Alignment.Bottom | Alignment.Center | Alignment.Top:
				dx = max(0, width - mask.shape[2])
				left = dx // 2
				right = dx - left

			case _:
				assert_never(alignment)

		match alignment:
			case Alignment.Top | Alignment.TopLeft | Alignment.TopRight:
				top = 0
				bottom = max(0, height - mask.shape[1])

			case Alignment.Bottom | Alignment.BottomLeft | Alignment.BottomRight:
				top = max(0, height - mask.shape[1])
				bottom = 0

			case Alignment.Center | Alignment.Left | Alignment.Right:
				dy = max(0, height - mask.shape[1])
				top = dy // 2
				bottom = dy - top

			case _:
				assert_never(alignment)

		return OneMaskPad.execute(
			mask = mask,
			top = top,
			right = right,
			bottom = bottom,
			left = left,
			value = kwargs["value"],
			device = kwargs["device"],
		)
