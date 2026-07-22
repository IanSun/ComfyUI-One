from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from typing import TypedDict, Unpack, assert_never
from ...shared.io import Alignment, OneAlignment
from .mask_pad import OneMaskPad

class OneMaskPadToMultipleInputs(TypedDict):
	alignment: Alignment
	device: str
	mask: Tensor
	multiple: int
	value: float

class OneMaskPadToMultiple(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskPadToMultiple",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
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
	def execute(cls, **kwargs: Unpack[OneMaskPadToMultipleInputs]) -> io.NodeOutput:
		alignment = kwargs["alignment"]
		mask = kwargs["mask"]
		multiple = kwargs["multiple"]

		match alignment:
			case Alignment.BottomLeft | Alignment.Left | Alignment.TopLeft:
				left = 0
				right = multiple - mask.shape[2] % multiple

			case Alignment.BottomRight | Alignment.Right | Alignment.TopRight:
				left = multiple - mask.shape[2] % multiple
				right = 0

			case Alignment.Bottom | Alignment.Center | Alignment.Top:
				dx = multiple - mask.shape[2] % multiple
				left = dx // 2
				right = dx - left

			case _:
				assert_never(alignment)

		match alignment:
			case Alignment.Top | Alignment.TopLeft | Alignment.TopRight:
				top = 0
				bottom = multiple - mask.shape[1] % multiple

			case Alignment.Bottom | Alignment.BottomLeft | Alignment.BottomRight:
				top = multiple - mask.shape[1] % multiple
				bottom = 0

			case Alignment.Center | Alignment.Left | Alignment.Right:
				dy = multiple - mask.shape[1] % multiple
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
