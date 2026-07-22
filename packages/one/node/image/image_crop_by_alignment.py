from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from typing import TypedDict, Unpack
from ...shared.type import Alignment, OneAlignment

class _Inputs(TypedDict):
	alignment: io.Combo.Type
	device: tuple[str, int] | io.Combo.Type
	height: io.Int.Type
	image: io.Image.Type
	width: io.Int.Type

class OneImageCropByAlignment(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageCropByAlignment",
			display_name = "图像裁剪（对齐）",
			category = "One/图像/变换",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
				),
				io.Int.Input(
					id = "width",
					display_name = "宽度",
					default = 1024,
					min = 0,
				),
				io.Int.Input(
					id = "height",
					display_name = "高度",
					default = 1024,
					min = 0,
				),
				OneAlignment.Input(
					id = "alignment",
					display_name = "对齐",
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					display_name = "设备",
					raw_link = True,
					advanced = True,
				),
			],
			outputs = [
				io.Image.Output(
					id = "image",
					display_name = "图像",
				),
				io.BoundingBox.Output(
					id = "box",
					display_name = "边界框",
				),
			],
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		image = kwargs["image"]

		_, h, w, _ = image.shape

		alignment = kwargs["alignment"]
		height, width = kwargs["height"], kwargs["width"]

		match alignment:
			case Alignment.BottomLeft | Alignment.Left | Alignment.TopLeft:
				x = 0

			case Alignment.BottomRight | Alignment.Right | Alignment.TopRight:
				x = max(0, w - width)

			case Alignment.Bottom | Alignment.Center | Alignment.Top:
				x = max(0, (w - width) // 2)

			case _:
				x = 0

		match alignment:
			case Alignment.Top | Alignment.TopLeft | Alignment.TopRight:
				y = 0

			case Alignment.Bottom | Alignment.BottomLeft | Alignment.BottomRight:
				y = max(0, h - height)

			case Alignment.Center | Alignment.Left | Alignment.Right:
				y = max(0, (h - height) // 2)

			case _:
				y = 0

		graph = GraphBuilder()
		one_image_crop = graph.node(
			"OneImageCrop",
			image = image,
			x = x,
			y = y,
			width = width,
			height = height,
			device = kwargs["device"],
		)

		return io.NodeOutput(
			one_image_crop.out(0),
			expand = graph.finalize(),
		)
