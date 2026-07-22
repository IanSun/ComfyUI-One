from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import float32, full
from typing import TypedDict, Unpack

class OneMaskInputs(TypedDict):
	batch: int
	device: str
	height: int
	value: float
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
				io.Float.Input(
					id = "value",
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
					default = "default",
					advanced = True,
				),
			],
			outputs = [
				io.Mask.Output(id = "mask"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskInputs]) -> io.NodeOutput:
		return io.NodeOutput(
			full(
				size = (kwargs["batch"], kwargs["height"], kwargs["width"]),
				fill_value = float(kwargs["value"]),
				dtype = float32,
				device = resolve_gpu_device_option(kwargs["device"]),
			)
		)
