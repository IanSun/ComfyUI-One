from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	device: io.Combo.Type
	mask: io.Mask.Type
	value: io.Float.Type

class OneMaskMultiply(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskMultiply",
			display_name = "遮罩乘法",
			category = "One/图像/遮罩",
			inputs = [
				io.Mask.Input(
					id = "mask",
					display_name = "遮罩",
				),
				io.Float.Input(
					id = "value",
					display_name = "数值",
					default = 1.0,
					min = 0.0,
					max = 1.0,
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

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			mask = mask.to(device)

		mask = mask * kwargs["value"]

		return io.NodeOutput(mask)
