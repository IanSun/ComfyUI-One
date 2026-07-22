from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	image: tuple[str, int]

class OneImageGetLongerEdge(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetLongerEdge",
			category = "One/Image",
			inputs = [
				io.Image.Input(
					id = "image",
					raw_link = True,
				),
			],
			outputs = [
				io.Int.Output(id = "edge"),
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
		one_int_max = graph.node(
			class_type = "OneIntMax",
			id = None,
			**{
				"value.value0": one_image_get_size.out(0),
				"value.value1": one_image_get_size.out(1),
			}
		)

		edge = one_int_max.out(0)

		return io.NodeOutput(
			edge,
			expand = graph.finalize(),
		)
