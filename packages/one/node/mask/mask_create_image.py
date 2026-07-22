from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from torch import Tensor, tensor
from typing import TypedDict, Unpack

class OneMaskCreateImageInputs(TypedDict):
	color: str
	device: str
	mask: Tensor

class OneMaskCreateImage(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskCreateImage",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
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
				io.Image.Output(id = "image"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskCreateImageInputs]) -> io.NodeOutput:
		color = kwargs["color"].lstrip("#")
		try:
			red, green, blue, *color_ = (value / 255.0 for value in bytes.fromhex(color))
			alpha = color_[0] if color_ else 1.0
		except ValueError:
			red, green, blue, alpha = 1.0, 1.0, 1.0, 1.0

		mask = kwargs["mask"]

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			mask = mask.to(device = device)

		weight = tensor(
			data = tuple(value * alpha for value in (red, green, blue)),
			dtype = mask.dtype,
			device = mask.device,
		)

		image = mask.unsqueeze(dim = -1) * weight

		return io.NodeOutput(image)
