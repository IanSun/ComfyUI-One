import torch
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from sys import maxsize
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	batch: int
	color: str
	device: str
	height: int
	width: int

class OneImage(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImage",
			category = "One/Image",
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
				io.Color.Input(
					id = "color",
					default = "#FFFFFF",
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
				io.Image.Output(id = "image"),
				io.Mask.Output(id = "mask"),
			],
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		height = int(kwargs["height"])
		width = int(kwargs["width"])

		image = None
		mask = None

		graph = GraphBuilder()

		if 0 < height or 0 < width:
			color = kwargs["color"].lstrip("#")
			try:
				r, g, b, *rest = (i / 255.0 for i in bytes.fromhex(color))
				a = rest[0] if rest else 1.0
			except ValueError:
				r, g, b, a = 1.0, 1.0, 1.0, 1.0

			batch = int(kwargs["batch"])
			device = kwargs["device"]

			image = torch.empty(
				size = (batch, height, width, 3),
				dtype = torch.float32,
				device = resolve_gpu_device_option(device),
			)
			image[..., 0] = r
			image[..., 1] = g
			image[..., 2] = b


			one_mask = graph.node(
				class_type = "OneMask",
				batch = batch,
				device = device,
				height = height,
				strength = 1.0 - a,
				width = width,
			)

			mask = one_mask.out(0)

		return io.NodeOutput(
			image,
			mask,
			expand = graph.finalize(),
		)
