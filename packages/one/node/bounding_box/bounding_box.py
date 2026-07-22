from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	height: io.Int.Type
	width: io.Int.Type
	x: io.Int.Type
	y: io.Int.Type

class OneBoundingBox(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneBoundingBox",
			display_name = "边界框",
			category = "One/图像/检测",
			inputs = [
				io.Int.Input(
					id = "x",
					display_name = "X",
				),
				io.Int.Input(
					id = "y",
					display_name = "Y",
				),
				io.Int.Input(
					id = "width",
					display_name = "宽度",
				),
				io.Int.Input(
					id = "height",
					display_name = "高度",
				),
			],
			outputs = [
				io.BoundingBox.Output(
					id = "box",
					display_name = "边界框",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		box: io.BoundingBox.Type = {
			"x": kwargs["x"],
			"y": kwargs["y"],
			"width": kwargs["width"],
			"height": kwargs["height"],
		}

		return io.NodeOutput(box)
