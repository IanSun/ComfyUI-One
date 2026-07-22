import torch
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	box: io.BoundingBoxes.Type
	device: io.Combo.Type
	height: io.Int.Type
	value: io.Float.Type
	width: io.Int.Type

class OneBoundingBoxCreateMask(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneBoundingBoxCreateMask",
			display_name = "边界框创建遮罩",
			category = "One/图像/遮罩",
			inputs = [
				io.Int.Input(
					id = "width",
					display_name = "宽度",
					min = 0,
				),
				io.Int.Input(
					id = "height",
					display_name = "高度",
					min = 0,
				),
				io.BoundingBoxes.Input(
					id = "box",
					display_name = "边界框",
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
				io.Mask.Output(
					id = "mask",
					display_name = "遮罩",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		height, width = kwargs["height"], kwargs["width"]

		mask = torch.zeros((1, height, width), device = resolve_gpu_device_option(kwargs["device"]))
		for b in kwargs["box"]:
			x, y, w, h = b["x"], b["y"], b["width"], b["height"]

			x1, y1 = max(0, min(x, width)), max(0, min(y, height))
			x2, y2 = max(0, min(x + w, width)), max(0, min(y + h, height))
			if x2 > x1 and y2 > y1:
				mask[0, y1:y2, x1:x2] = kwargs["value"]

		return io.NodeOutput(mask)
