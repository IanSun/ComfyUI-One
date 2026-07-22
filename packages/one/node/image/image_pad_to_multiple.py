import math
import torch
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from typing import TypedDict, Unpack
from ...shared.type import Alignment, OneAlignment

class _Inputs(TypedDict):
	alignment: io.Combo.Type
	device: io.Combo.Type
	image: io.Image.Type
	multiple: io.Int.Type

class OneImagePadToMultiple(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImagePadToMultiple",
			display_name = "图像外补（倍数）",
			category = "One/图像/缩放",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
				),
				io.Int.Input(
					id = "multiple",
					display_name = "倍数",
					min = 1,
					default = 8,
				),
				OneAlignment.Input(
					id = "alignment",
					display_name = "对齐",
					default = Alignment.TopLeft,
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					display_name = "设备",
					advanced = True,
				),
			],
			outputs = [
				io.Image.Output(
					id = "image",
					display_name = "图像",
				),
				io.BoundingBox.Output(
					id = "box",
					display_name = "边界框",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		image = kwargs["image"]

		_, h, w, _ = image.shape

		box: io.BoundingBox.Type = {
			"x": 0,
			"y": 0,
			"width": w,
			"height": h,
		}

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			image = image.to(device)

		multiple = kwargs["multiple"]

		if 0 != h % multiple or 0 != w % multiple:
			ph, pw = math.ceil(h / multiple) * multiple - h, math.ceil(w / multiple) * multiple - w

			alignment = kwargs["alignment"]

			match alignment:
				case Alignment.BottomLeft | Alignment.Left | Alignment.TopLeft:
					pl = 0
					pr = pw

				case Alignment.BottomRight | Alignment.Right | Alignment.TopRight:
					pl = pw
					pr = 0

				case Alignment.Bottom | Alignment.Center | Alignment.Top:
					pl = pw // 2
					pr = pw - pl

				case _:
					pl = 0
					pr = pw

			match alignment:
				case Alignment.Top | Alignment.TopLeft | Alignment.TopRight:
					pt = 0
					pb = ph

				case Alignment.Bottom | Alignment.BottomLeft | Alignment.BottomRight:
					pt = ph
					pb = 0

				case Alignment.Center | Alignment.Left | Alignment.Right:
					pt = ph // 2
					pb = ph - pt

				case _:
					pt = 0
					pb = ph

			image = torch.nn.functional.pad(image, (0, 0, pl, pr, pt, pb))

			box["x"] = pl
			box["y"] = pt

		return io.NodeOutput(image, box)
