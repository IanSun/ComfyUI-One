from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	box: io.BoundingBox.Type

class OneBoundingBoxGetProperty(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneBoundingBoxGetProperty",
			display_name = "边界框获取属性",
			category = "One/图像/检测",
			inputs = [
				io.BoundingBox.Input(
					id = "box",
					display_name = "边界框",
				),
			],
			outputs = [
				io.Int.Output(
					id = "x",
					display_name = "X",
				),
				io.Int.Output(
					id = "y",
					display_name = "Y",
				),
				io.Int.Output(
					id = "width",
					display_name = "宽度",
				),
				io.Int.Output(
					id = "height",
					display_name = "高度",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		box = kwargs["box"]

		return io.NodeOutput(
			box["x"],
			box["y"],
			box["width"],
			box["height"],
		)
