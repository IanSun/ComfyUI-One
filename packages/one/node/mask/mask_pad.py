from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from torch.nn.functional import pad
from typing import TypedDict, Unpack

class OneMaskPadInputs(TypedDict):
	bottom: int
	device: str
	left: int
	mask: Tensor
	right: int
	top: int
	value: float

class OneMaskPad(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskPad",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
				io.Int.Input(
					id = "top",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "right",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "bottom",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "left",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
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
	def execute(cls, **kwargs: Unpack[OneMaskPadInputs]) -> io.NodeOutput:
		mask = kwargs["mask"]

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			mask = mask.to(device = device)

		bottom = kwargs["bottom"]
		left = kwargs["left"]
		right = kwargs["right"]
		top = kwargs["top"]

		if 0 == bottom == left == right == top:
			return io.NodeOutput(mask)

		mask = pad(
			input = mask,
			pad = (left, right, top, bottom),
			value = kwargs["value"],
		)

		return io.NodeOutput(mask)
