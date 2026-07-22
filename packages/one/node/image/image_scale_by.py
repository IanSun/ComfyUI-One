from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from torch.nn.functional import interpolate
from typing import TypedDict, Unpack
from ...shared.io import OneScaleMethod, ScaleMethod

class OneImageScaleByInputs(TypedDict):
	device: str
	image: Tensor
	method: ScaleMethod
	multiple: float

class OneImageScaleBy(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageScaleBy",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
				OneScaleMethod.Input(id = "method"),
				io.Float.Input(
					id = "multiple",
					default = 1.0,
					min = 0.0,
					max = maxsize,
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
				io.Image.Output(id = "image"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageScaleByInputs]) -> io.NodeOutput:
		image = kwargs["image"]
		multiple = kwargs["multiple"]

		device = resolve_gpu_device_option(kwargs["device"])

		if 1.0 == multiple:
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
			scale_factor = multiple,
			mode = method,
			antialias = method in [ScaleMethod.Bicubic, ScaleMethod.Bilinear, ScaleMethod.Lanczos],
		)

		if force_cpu:
			image = image.to(image_device if device is None else device)

		return io.NodeOutput(image)
