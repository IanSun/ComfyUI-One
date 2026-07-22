from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	box: io.BoundingBox.Type
	device: tuple[str, int] | io.Combo.Type
	image: tuple[str, int]

class OneImageCropByBoundingBox(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageCropByBoundingBox",
			display_name = "图像裁剪（边界框）",
			category = "One/图像/变换",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
					raw_link = True,
				),
				io.BoundingBox.Input(
					id = "box",
					display_name = "边界框",
					default = {
						"x": 0,
						"y": 0,
						"width": 0,
						"height": 0,
					},
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
			],
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		graph = GraphBuilder()
		one_bounding_box_get_property = graph.node(
			"OneBoundingBoxGetProperty",
			box = kwargs["box"],
		)
		one_image_crop = graph.node(
			"OneImageCrop",
			image = kwargs["image"],
			x = one_bounding_box_get_property.out(0),
			y = one_bounding_box_get_property.out(1),
			width = one_bounding_box_get_property.out(2),
			height = one_bounding_box_get_property.out(3),
			device = kwargs["device"],
		)

		return io.NodeOutput(
			one_image_crop.out(0),
			expand = graph.finalize(),
		)
