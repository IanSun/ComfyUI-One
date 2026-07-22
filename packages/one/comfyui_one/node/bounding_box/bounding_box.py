from comfy_api.latest import io
from sys import maxsize
from typing import TypedDict, Unpack

class OneBoundingBoxInputs(TypedDict):
	height: int
	width: int
	x: int
	y: int

class OneBoundingBox(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneBoundingBox",
			category = "One/BoundingBox",
			inputs = [
				io.Int.Input(
					id = "x",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "y",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
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
			],
			outputs = [
				io.BoundingBox.Output(id = "box"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneBoundingBoxInputs]) -> io.NodeOutput:
		return io.NodeOutput({
			"x": kwargs["x"],
			"y": kwargs["y"],
			"width": kwargs["width"],
			"height": kwargs["height"],
		})
