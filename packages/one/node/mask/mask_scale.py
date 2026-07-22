from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor
from torch.nn.functional import interpolate
from typing import TypedDict, Unpack
from ...shared.io import OneScaleMethod, ScaleMethod

class OneMaskScaleInputs(TypedDict):
	device: str
	height: int
	mask: Tensor
	method: ScaleMethod
	width: int

class OneMaskScale(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskScale",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
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
				io.Mask.Output(id = "mask"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskScaleInputs]) -> io.NodeOutput:
		height = kwargs["height"]
		mask = kwargs["mask"]
		width = kwargs["width"]

		shape = mask.shape
		device = resolve_gpu_device_option(kwargs["device"])

		if shape[1:3] == (height, width):
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
				size = (height, width),
				mode = method,
				antialias = method in [ScaleMethod.Bicubic, ScaleMethod.Bilinear, ScaleMethod.Lanczos],
			)
			.squeeze(1)
		)

		if force_cpu:
			mask = mask.to(mask_device if device is None else device)

		return io.NodeOutput(mask)
