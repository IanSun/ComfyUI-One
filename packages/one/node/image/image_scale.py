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
	image: io.Image.Type
	method: io.Combo.Type
	width: io.Int.Type

class OneImageScale(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageScale",
			display_name = "图像缩放",
			category = "One/图像/缩放",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
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
				io.Image.Output(
					id = "image",
					display_name = "图像",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		image = kwargs["image"]

		_, h, w, _ = image.shape
		d = image.device

		height, width = kwargs["height"], kwargs["width"]
		device = resolve_gpu_device_option(kwargs["device"])

		if h == height and w == width:
			if device is not None:
				image = image.to(device)

		else:
			method = kwargs["method"]

			if Method.Lanczos == method:
				image = image.to("cpu")
			elif device is not None:
				image = image.to(device)

			image = (torch.nn.functional
				.interpolate(
					image.movedim(-1, 1),
					(height, width),
					mode = method,
					antialias = method in [Method.Bicubic, Method.Bilinear, Method.Lanczos],
				)
				.movedim(1, -1)
			)

			if Method.Lanczos == method:
				image = image.to(d if device is None else device)

			image = image.contiguous()

		return io.NodeOutput(image)
