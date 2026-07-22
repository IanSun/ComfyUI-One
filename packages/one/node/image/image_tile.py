import math
import torch
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from enum import StrEnum
from typing import TypedDict, Unpack, cast

class Alignment(StrEnum):
	TopLeft = "左上对齐"
	Top = "上对齐"
	TopRight = "右上对齐"
	Left = "左对齐"
	Center = "中心对齐"
	Right = "右对齐"
	BottomLeft = "左下对齐"
	Bottom = "下对齐"
	BottomRight = "右下对齐"

class _Inputs(TypedDict):
	alignment: io.Combo.Type
	device: io.Combo.Type
	height: io.Int.Type
	image: io.Image.Type
	overlap: io.Int.Type
	width: io.Int.Type

class OneImageTile(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageTile",
			display_name = "图像分块",
			category = "One/图像/批处理",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
				),
				io.Int.Input(
					id = "width",
					display_name = "分块宽度",
					default = 1024,
					min = 1,
				),
				io.Int.Input(
					id = "height",
					display_name = "分块高度",
					default = 1024,
					min = 1,
				),
				io.Int.Input(
					id = "overlap",
					display_name = "重叠尺寸",
					default = 128,
					min = 0,
				),
				io.Combo.Input(
					id = "alignment",
					options = Alignment,
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
				io.BoundingBoxes.Output(
					id = "box",
					display_name = "边界框",
				),
				io.Int.Output(
					id = "row",
					display_name = "行",
				),
				io.Int.Output(
					id = "column",
					display_name = "列",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		image = kwargs["image"]
		alignment = kwargs.get("alignment")
		height = kwargs.get("height")
		width = kwargs.get("width")

		b, h, w, _ = image.shape

		overlap = kwargs["overlap"]
		oh, ow = min(overlap, height // 2), min(overlap, width // 2)

		sh, sw = height - oh, width - ow
		row, column = (
			math.ceil((h - oh) / sh) if h > oh else 1,
			math.ceil((w - ow) / sw) if w > ow else 1,
		)

		ph, pw = sh * (row - 1) + height - h, sw * (column - 1) + width - w

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			image = image.to(device)

		sy, sx = (
			torch.arange(0, row, device = image.device) * sh,
			torch.arange(0, column, device = image.device) * sw,
		)
		gy, gx = torch.meshgrid(sy, sx, indexing = "ij")
		gy, gx = gy.flatten(), gx.flatten()

		if 0 < ph or 0 < pw:
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

			x1, x2 = torch.clamp(pl - gx, 0, width), torch.clamp(pl - gx + w, 0, width)
			y1, y2 = torch.clamp(pt - gy, 0, height), torch.clamp(pt - gy + h, 0, height)
			x, y, tw, th = x1, y1, torch.clamp(x2 - x1, 0), torch.clamp(y2 - y1, 0)
		else:
			x, y, tw, th = (
				gx,
				gy,
				torch.full_like(gx, width, device = image.device),
				torch.full_like(gy, height, device = image.device),
			)

		image = (image
			.unfold(1, height, sh)
			.unfold(2, width, sw)
			.permute(0, 1, 2, 4, 5, 3)
			.flatten(0, 2)
		)

		box: io.BoundingBoxes.Type = [
			{
				"x": i[0],
				"y": i[1],
				"width": i[2],
				"height": i[3],
			}
			for i in cast(
				list[list[int]],
				torch
					.stack([x, y, tw, th], -1)
					.unsqueeze(0)
					.expand(b, -1, -1)
					.reshape(-1, 4)
					.cpu()
					.tolist() # pyright: ignore[reportUnknownMemberType]
			)
		]

		return io.NodeOutput(image, box, row, column)
