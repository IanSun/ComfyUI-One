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
		graph = GraphBuilder()

		one_image_get_size = graph.node(
			class_type = "OneImageGetSize",
			image = kwargs["image"],
		)
		one_int_multiply = graph.node(
			class_type = "OneIntMultiply",
			id = None,
			**{
				"value.value0": one_image_get_size.out(0),
				"value.value1": one_image_get_size.out(1),
			}
		)

		resolution = one_int_multiply.out(0)

		return io.NodeOutput(
			resolution,
			expand = graph.finalize(),
		)
