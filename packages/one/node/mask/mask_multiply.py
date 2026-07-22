from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack

class OneMaskMultiplyInputs(TypedDict):
	device: str
	mask: Tensor
	value: float

class OneMaskMultiply(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskMultiply",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
				io.Float.Input(
					id = "value",
					default = 1.0,
					min = 0.0,
					max = 1.0,
					step = 0.01,
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					default = "default",
					raw_link = True,
					advanced = True,
				),
			],
			outputs = [
				io.Mask.Output(id = "mask"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskMultiplyInputs]) -> io.NodeOutput:
		mask = kwargs["mask"]

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			mask = mask.to(device = device)

		mask *= kwargs["value"]

		return io.NodeOutput(mask)
