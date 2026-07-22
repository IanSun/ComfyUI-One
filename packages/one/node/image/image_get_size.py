from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	image: tuple[str, int]

class OneImageGetSize(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetSize",
			category = "One/Image",
			inputs = [
				io.Image.Input(
					id = "image",
					raw_link = True,
				),
			],
			outputs = [
				io.Int.Output(id = "width"),
				io.Int.Output(id = "height"),
			],
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		image = kwargs["image"]

		graph = GraphBuilder()

		one_image_get_height = graph.node(
			class_type = "OneImageGetHeight",
			image = image,
		)
		one_image_get_width = graph.node(
			class_type = "OneImageGetWidth",
			image = image,
		)

		width = one_image_get_width.out(0)
		height = one_image_get_height.out(0)

		return io.NodeOutput(
			width,
			height,
			expand = graph.finalize(),
		)
