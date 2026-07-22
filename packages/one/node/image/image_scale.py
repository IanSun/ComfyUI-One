from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from torch.nn.functional import interpolate
from typing import TypedDict, Unpack
from ...shared.io import OneScaleMethod, ScaleMethod

class OneImageScaleInputs(TypedDict):
	device: str
	height: int
	image: Tensor
	method: ScaleMethod
	width: int

class OneImageScale(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageScale",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
				OneScaleMethod.Input(id = "method"),
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
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					default = "default",
					advanced = True,
				),
			],
			outputs = [
				io.Image.Output(id = "image"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageScaleInputs]) -> io.NodeOutput:
		height = kwargs["height"]
		image = kwargs["image"]
		width = kwargs["width"]

		shape = image.shape
		device = resolve_gpu_device_option(kwargs["device"])

		if shape[1:3] == (height, width):
			if device is not None:
				image = image.to(device = device)

			return io.NodeOutput(image)

		method = kwargs["method"]

		force_cpu = ScaleMethod.Lanczos == method
		image_device = image.device

		if force_cpu:
			image = image.to(device = "cpu")
		elif device is not None:
			image = image.to(device)

		image = interpolate(
			input = image,
			size = (height, width),
			mode = method,
			antialias = method in [ScaleMethod.Bicubic, ScaleMethod.Bilinear, ScaleMethod.Lanczos],
		)

		if force_cpu:
			image = image.to(image_device if device is None else device)

		return io.NodeOutput(image)
