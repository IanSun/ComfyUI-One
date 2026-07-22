from comfy_api.latest import io
from sys import maxsize
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
			category = "One/Primitive",
			inputs = [
				io.Int.Input(
					id = "x",
					default = 0,
					min = 0,
					max = maxsize,
				),
				io.Int.Input(
					id = "y",
					default = 0,
					min = 0,
					max = maxsize,
				),
				io.Int.Input(
					id = "width",
					default = 0,
					min = 0,
					max = maxsize,
				),
				io.Int.Input(
					id = "height",
					default = 0,
					min = 0,
					max = maxsize,
				),
			],
			outputs = [
				io.BoundingBox.Output(id = "box"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		box: io.BoundingBox.Type = {
			"x": int(kwargs["x"]),
			"y": int(kwargs["y"]),
			"width": int(kwargs["width"]),
			"height": int(kwargs["height"]),
		}

		return io.NodeOutput(box)
