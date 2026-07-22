from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	image: tuple[str, int]

class OneImageGetResolution(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetResolution",
			category = "One/Image",
			inputs = [
				io.Image.Input(
					id = "image",
					raw_link = True,
				),
			],
			outputs = [
				io.Int.Output(id = "resolution"),
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
		one_int_multiply = graph.node(
			class_type = "OneIntMultiply",
			id = None,
			**{
				"factor.factor0": one_image_get_height.out(0),
				"factor.factor1": one_image_get_width.out(0),
			}
		)

		resolution = one_int_multiply.out(0)

		return io.NodeOutput(
			resolution,
			expand = graph.finalize(),
		)
