from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from enum import StrEnum
from typing import TypedDict, Unpack
from .image_scale import Method

class Edge(StrEnum):
	Long = "长边"
	Short = "短边"

class _Inputs(TypedDict):
	device: tuple[str, int] | io.Combo.Type
	edge: io.Combo.Type
	image: io.Image.Type
	length: io.Int.Type
	method: tuple[str, int] | io.Combo.Type

class OneImageScaleByEdge(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageScaleByEdge",
			display_name = "图像缩放（边）",
			category = "One/图像/缩放",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
				),
				io.Combo.Input(
					id = "method",
					options = Method,
					display_name = "缩放算法",
					default = Method.Lanczos,
					raw_link = True,
				),
				io.Combo.Input(
					id = "edge",
					options = Edge,
					display_name = "边",
					default = Edge.Long,
				),
				io.Int.Input(
					id = "length",
					display_name = "长度",
					min = 0,
					default = 1024,
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					display_name = "设备",
					raw_link = True,
					advanced = True,
				),
			],
			outputs = [
				io.Image.Output(
					id = "image",
					display_name = "图像",
				),
			],
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		image = kwargs["image"]

		_, h, w, _ = image.shape

		match kwargs["edge"]:
			case Edge.Long:
				l = max(h, w)

			case Edge.Short:
				l = min(h, w)

			case _:
				l = max(h, w)

		length = kwargs["length"]

		if length == l:
			return io.NodeOutput(image)

		r = length / l

		graph = GraphBuilder()
		one_image_scale = graph.node(
			"OneImageScale",
			image = image,
			method = kwargs["method"],
			width = round(w * r),
			height = round(h * r),
			device = kwargs["device"],
		)

		return io.NodeOutput(
			one_image_scale.out(0),
			expand = graph.finalize(),
		)
