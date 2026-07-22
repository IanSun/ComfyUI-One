from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from torch import Tensor, finfo, tensor
from typing import TypedDict, Unpack

class OneImageCreateMaskInputs(TypedDict):
	color: str
	device: str
	image: Tensor

class OneImageCreateMask(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageCreateMask",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
				io.Color.Input(
					id = "color",
					default = "#FFFFFF",
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
	def execute(cls, **kwargs: Unpack[OneImageCreateMaskInputs]) -> io.NodeOutput:
		color = kwargs["color"].lstrip("#")
		try:
			red, green, blue, *color_ = (value / 255.0 for value in bytes.fromhex(color))
			alpha = color_[0] if color_ else 1.0
		except ValueError:
			red, green, blue, alpha = 1.0, 1.0, 1.0, 1.0

		image = kwargs["image"]

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			image = image.to(device = device)

		weight = tensor(
			data = tuple(value * alpha for value in (red, green, blue)),
			dtype = image.dtype,
			device = image.device,
		)

		mask = (image * weight).sum(dim = -1) / weight.square().sum().clamp_min_(min = finfo(image.dtype).eps)

		return io.NodeOutput(mask)
