from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	box: io.BoundingBoxes.Type
	multiplier: io.Float.Type

class OneBoundingBoxScale(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneBoundingBoxScale",
			display_name = "边界框缩放",
			category = "One/图像/检测",
			inputs = [
				io.BoundingBoxes.Input(
					id = "box",
					display_name = "边界框",
				),
				io.Float.Input(
					id = "multiplier",
					display_name = "倍数",
					default = 1,
					min = 0,
				),
			],
			outputs = [
				io.BoundingBoxes.Output(
					id = "box",
					display_name = "边界框",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		multiplier = kwargs["multiplier"]

		box: io.BoundingBoxes.Type = [
			{
				"x": round(b["x"] * multiplier),
				"y": round(b["y"] * multiplier),
				"width": round(b["width"] * multiplier),
				"height": round(b["height"] * multiplier),
			}
			for b in kwargs["box"]
		]

		return io.NodeOutput(box)
