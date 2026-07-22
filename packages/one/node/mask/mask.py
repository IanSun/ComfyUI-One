import torch
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	batch: int
	device: str
	height: int
	strength: float
	width: int

class OneMask(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMask",
			category = "One/Mask",
			inputs = [
				io.Int.Input(
					id = "width",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "height",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Float.Input(
					id = "strength",
					default = 1.0,
					min = 0.0,
					max = 1.0,
					step = 0.01,
				),
				io.Int.Input(
					id = "batch",
					default = 1,
					min = 1,
					max = maxsize,
					step = 1,
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					advanced = True,
				),
			],
			outputs = [
				io.Mask.Output(id = "mask"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		height = int(kwargs["height"])
		width = int(kwargs["width"])

		mask = None
		if 0 < height or 0 < width:
			mask = torch.full(
				size = (int(kwargs["batch"]), height, width),
				fill_value = float(kwargs["strength"]),
				dtype = torch.float32,
				device = resolve_gpu_device_option(kwargs["device"]),
			)

		return io.NodeOutput(mask)
