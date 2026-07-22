import math
import torch
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from typing import TypedDict, Unpack, cast

class _Inputs(TypedDict):
	box: io.BoundingBoxes.Type | None
	column: io.Int.Type
	device: io.Combo.Type
	image: io.Image.Type
	overlap: io.Int.Type
	row: io.Int.Type

class OneImageStitch(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageStitch",
			display_name = "图像拼接",
			category = "One/图像/变换",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
				),
				io.BoundingBoxes.Input(
					id = "box",
					display_name = "边界框",
					optional = True,
				),
				io.Int.Input(
					id = "row",
					display_name = "行",
					default = 1,
					min = 1,
				),
				io.Int.Input(
					id = "column",
					display_name = "列",
					default = 1,
					min = 1,
				),
				io.Int.Input(
					id = "overlap",
					display_name = "重叠尺寸",
					default = 128,
					min = 0,
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
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		image = kwargs["image"]

		batch, height, width, channel = image.shape

		overlap = kwargs["overlap"]
		oh, ow = min(overlap, height // 2), min(overlap, width // 2)

		column, row = kwargs["column"], kwargs["row"]
		size = row * column

		b = math.ceil(batch / size)

		sh, sw = height - oh, width - ow
		h, w = sh * row + oh, sw * column + ow

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			image = image.to(device)

		zero = torch.zeros((height, width, channel), dtype = image.dtype, device = image.device)

		canvas = torch.zeros((b, h, w, channel), dtype = image.dtype, device = image.device)
		mask = torch.zeros((b, h, w, 1), dtype = image.dtype, device = image.device)
		weight = torch.ones((height, width, 1), dtype = image.dtype, device = image.device)

		oh, ow = oh if 1 < row else 0, ow if 1 < column else 0

		if 0 < ow:
			base = torch.linspace(0.0, torch.pi, ow, dtype = image.dtype, device = image.device)
			weight[:, :ow, :] = torch.minimum(weight[:, :ow, :], ((1.0 - torch.cos(base)) * 0.5).view(1, ow, 1))
			weight[:, -ow:, :] = torch.minimum(weight[:, -ow:, :], ((1.0 + torch.cos(base)) * 0.5).view(1, ow, 1))

		if 0 < oh:
			base = torch.linspace(0.0, torch.pi, oh, dtype = image.dtype, device = image.device)
			weight[:oh, :, :] = torch.minimum(weight[:oh, :, :], ((1.0 - torch.cos(base)) * 0.5).view(oh, 1, 1))
			weight[-oh:, :, :] = torch.minimum(weight[-oh:, :, :], ((1.0 + torch.cos(base)) * 0.5).view(oh, 1, 1))

		box = kwargs.get("box")
		bl = None if box is None else len(box) - 1

		for i in range(b):
			for r in range(row):
				for c in range(column):
					index = i * size + r * column + c

					x1, y1 = sw * c, sh * r
					x2, y2 = x1 + width, y1 + height

					if box is None:
						tw = weight

					else:
						ib = box[min(index, cast(int, bl))]
						bx1, by1, bw, bh = ib["x"], ib["y"], ib["width"], ib["height"]
						bx2, by2 = bx1 + bw, by1 + bh

						tw = weight.clone()
						tw[:, :bx1, :] = 0.0
						tw[:, bx2:, :] = 0.0
						tw[:by1, :, :] = 0.0
						tw[by2:, :, :] = 0.0

					canvas[i, y1:y2, x1:x2, :] += (image[index] if index < batch else zero) * tw
					mask[i, y1:y2, x1:x2, :] += tw

		image = torch.where(0 < mask, canvas / mask, torch.tensor(0.0, image.dtype, image.device))

		if box is not None:
			b0, bs = box[0], box[min(size - 1, cast(int, bl))]
			image = image[
				:,
				b0["y"]:h - height + bs["height"],
				b0["x"]:w - width + bs["width"],
				:,
			]

		return io.NodeOutput(image)
