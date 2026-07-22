import math
import torch
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	box: io.BoundingBoxes.Type | None
	column: io.Int.Type
	device: io.Combo.Type
	latent: io.Latent.Type
	overlap: io.Int.Type
	row: io.Int.Type

class OneLatentStitch(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneLatentStitch",
			display_name = "Latent拼接",
			category = "One/模型/Latent/变换",
			inputs = [
				io.Latent.Input(
					id = "latent",
					display_name = "潜空间",
				),
				io.BoundingBoxes.Input(
					id = "box",
					display_name = "边界框",
					optional = True,
				),
				io.Int.Input(
					id = "row",
					display_name = "行",
					min = 1,
				),
				io.Int.Input(
					id = "column",
					display_name = "列",
					min = 1,
				),
				io.Int.Input(
					id = "overlap",
					display_name = "重叠尺寸",
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
				io.Latent.Output(
					id = "latent",
					display_name = "潜空间",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		latent = kwargs["latent"]

		samples = latent["samples"]
		noise = latent.get("noise_mask")

		batch, channel, height, width = samples.shape

		overlap = kwargs["overlap"]
		oh, ow = min(overlap, height // 2), min(overlap, width // 2)

		column, row = kwargs["column"], kwargs["row"]
		size = row * column

		b = math.ceil(batch / size)

		sh, sw = height - oh, width - ow
		h, w = sh * row + oh, sw * column + ow

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			samples = samples.to(device)

			if noise is not None:
				noise = noise.to(device)

		if noise is not None:
			if height != noise.shape[1] or width != noise.shape[2]:
				noise = (torch.nn.functional
					.interpolate(
						noise.unsqueeze(1),
						(height, width),
						mode = "nearest-exact",
					)
					.squeeze(1)
				)

			nbatch = noise.shape[0]
			if batch > nbatch:
				noise = noise[torch.arange(batch, device = noise.device) % nbatch]
			elif batch < nbatch:
				noise = noise[:batch]

		zero = torch.zeros((channel, height, width), dtype = samples.dtype, device = samples.device)
		nzero = None if noise is None else torch.zeros((height, width), dtype = noise.dtype, device = noise.device)

		canvas = torch.zeros((b, channel, h, w), dtype = samples.dtype, device = samples.device)
		ncanvas = None if noise is None else torch.zeros((b, h, w), dtype = noise.dtype, device = noise.device)

		mask = torch.zeros((b, 1, h, w), dtype = samples.dtype, device = samples.device)
		weight = torch.ones((1, height, width), dtype = samples.dtype, device = samples.device)

		oh, ow = oh if 1 < row else 0, ow if 1 < column else 0

		if 0 < ow:
			base = torch.linspace(0.0, torch.pi, ow, dtype = samples.dtype, device = samples.device)
			weight[:, :, :ow] = torch.minimum(weight[:, :, :ow], ((1.0 - torch.cos(base)) * 0.5).view(1, 1, ow))
			weight[:, :, -ow:] = torch.minimum(weight[:, :, -ow:], ((1.0 + torch.cos(base)) * 0.5).view(1, 1, ow))

		if 0 < oh:
			base = torch.linspace(0.0, torch.pi, oh, dtype = samples.dtype, device = samples.device)
			weight[:, :oh, :] = torch.minimum(weight[:, :oh, :], ((1.0 - torch.cos(base)) * 0.5).view(1, oh, 1))
			weight[:, -oh:, :] = torch.minimum(weight[:, -oh:, :], ((1.0 + torch.cos(base)) * 0.5).view(1, oh, 1))

		box = kwargs.get("box")
		bl = None if box is None else len(box) - 1

		for i in range(b):
			for r in range(row):
				for c in range(column):
					index = i * size + r * column + c

					x1, y1 = sw * c, sh * r
					x2, y2 = x1 + width, y1 + height

					if box is None or bl is None:
						tw = weight

					else:
						ib = box[min(index, bl)]
						bx1, by1, bw, bh = ib["x"], ib["y"], ib["width"], ib["height"]
						bx2, by2 = bx1 + bw, by1 + bh

						tw = weight.clone()
						tw[:, :, :bx1] = 0.0
						tw[:, :, bx2:] = 0.0
						tw[:, :by1, :] = 0.0
						tw[:, by2:, :] = 0.0

					canvas[i, :, y1:y2, x1:x2] += (samples[index] if index < batch else zero) * tw
					mask[i, :, y1:y2, x1:x2] += tw

					if noise is not None and nzero is not None and ncanvas is not None:
						ncanvas[i, y1:y2, x1:x2] += (noise[index] if index < batch else nzero) * tw[0]

		samples = torch.where(0 < mask, canvas / mask, torch.tensor(0.0, samples.dtype, samples.device))

		if noise is not None and ncanvas is not None:
			noise = torch.where(0 < mask.squeeze(1), ncanvas / mask.squeeze(1), torch.tensor(0.0, noise.dtype, noise.device))

		if box is not None and bl is not None:
			b0, bs = box[0], box[min(size - 1, bl)]
			x1, x2, y1, y2 = b0["x"], w - width + bs["width"], b0["y"], h - height + bs["height"]

			samples = samples[:, :, y1:y2, x1:x2]

			if noise is not None:
				noise = noise[:, y1:y2, x1:x2]

		l: io.Latent.Type = latent.copy()
		l["samples"] = samples

		if noise is not None:
			l["noise_mask"] = noise

		return io.NodeOutput(l)
