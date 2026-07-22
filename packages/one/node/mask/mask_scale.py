import torch
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from enum import StrEnum
from typing import TypedDict, Unpack

class Method(StrEnum):
	Area = "area"
	Bicubic = "bicubic"
	Bilinear = "bilinear"
	Lanczos = "lanczos"
	Nearest = "nearest"
	NearestExact = "nearest-exact"

class _Inputs(TypedDict):
	device: io.Combo.Type
	height: io.Int.Type
	mask: io.Mask.Type
	method: io.Combo.Type
	width: io.Int.Type

class OneMaskScale(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskScale",
			display_name = "遮罩缩放",
			category = "One/图像/遮罩/缩放",
			inputs = [
				io.Mask.Input(
					id = "mask",
					display_name = "遮罩",
				),
				io.Combo.Input(
					id = "method",
					options = Method,
					display_name = "缩放算法",
					default = Method.Lanczos,
				),
				io.Int.Input(
					id = "width",
					display_name = "宽度",
					default = 1024,
					min = 0,
				),
				io.Int.Input(
					id = "height",
					display_name = "高度",
					default = 1024,
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
				io.Mask.Output(
					id = "mask",
					display_name = "遮罩",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		mask = kwargs["mask"]

		_, h, w = mask.shape
		d = mask.device

		height, width = kwargs["height"], kwargs["width"]
		device = resolve_gpu_device_option(kwargs["device"])

		if h == height and w == width:
			if device is not None:
				mask = mask.to(device)

		else:
			method = kwargs["method"]

			if Method.Lanczos == method:
				mask = mask.to("cpu")
			elif device is not None:
				mask = mask.to(device)

			mask = (torch.nn.functional
				.interpolate(
					mask.unsqueeze(1),
					(height, width),
					mode = method,
					antialias = method in [Method.Bicubic, Method.Bilinear, Method.Lanczos],
				)
				.squeeze(1)
			)

			if Method.Lanczos == method:
				mask = mask.to(d if device is None else device)

			mask = mask.contiguous()

		return io.NodeOutput(mask)
