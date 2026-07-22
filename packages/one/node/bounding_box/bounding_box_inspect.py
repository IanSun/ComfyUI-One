from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	box: io.BoundingBox.Type

class OneBoundingBoxInspect(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneBoundingBoxInspect",
			category = "One/BoundingBox",
			inputs = [
				io.BoundingBox.Input(
					id = "box",
					force_input = True,
				),
			],
			outputs = [
				io.Int.Output(id = "x"),
				io.Int.Output(id = "y"),
				io.Int.Output(id = "width"),
				io.Int.Output(id = "height"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		box = kwargs["box"]

		x = box["x"]
		y = box["y"]
		width = box["width"]
		height = box["height"]

		return io.NodeOutput(
			x,
			y,
			width,
			height,
		)
