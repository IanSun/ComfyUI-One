from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from torch.nn.functional import interpolate
from typing import TypedDict, Unpack
from ...shared.io import OneScaleMethod, ScaleMethod

class OneMaskScaleByInputs(TypedDict):
	device: str
	mask: Tensor
	method: ScaleMethod
	multiple: float

class OneMaskScaleBy(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskScaleBy",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
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
				io.Mask.Output(id = "mask"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskScaleByInputs]) -> io.NodeOutput:
		mask = kwargs["mask"]
		multiple = kwargs["multiple"]

		device = resolve_gpu_device_option(kwargs["device"])

		if 1.0 == multiple:
			if device is not None:
				mask = mask.to(device = device)

			return io.NodeOutput(mask)

		method = kwargs["method"]

		force_cpu = ScaleMethod.Lanczos == method
		mask_device = mask.device

		if force_cpu:
			mask = mask.to(device = "cpu")
		elif device is not None:
			mask = mask.to(device)

		mask = (
			interpolate(
				input = mask.unsqueeze(1),
				scale_factor = multiple,
				mode = method,
				antialias = method in [ScaleMethod.Bicubic, ScaleMethod.Bilinear, ScaleMethod.Lanczos],
			)
			.squeeze(1)
		)

		if force_cpu:
			mask = mask.to(mask_device if device is None else device)

		return io.NodeOutput(mask)
