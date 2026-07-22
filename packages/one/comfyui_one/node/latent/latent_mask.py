from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	device: io.Combo.Type
	mask: io.Mask.Type
	latent: io.Latent.Type
	value: io.Float.Type

class OneLatentMask(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneLatentMask",
			display_name = "设置Latent噪波遮罩",
			category = "One/模型/Latent",
			inputs = [
				io.Latent.Input(
					id = "latent",
					display_name = "Latent",
				),
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
					advanced = True,
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
					display_name = "Latent",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		latent = kwargs["latent"]
		mask = kwargs["mask"]

		samples = latent["samples"]

		b, mb = samples.shape[0], mask.shape[0]

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			mask = mask.to(device)

		mask = mask * kwargs["value"]

		if b < mb:
			mask = mask[:b]
		elif b > mb:
			mask = mask.repeat((b + mb - 1) // mb, 1, 1)[:b]

		l: io.Latent.Type = latent.copy()
		l["noise_mask"] = mask

		return io.NodeOutput(l)
