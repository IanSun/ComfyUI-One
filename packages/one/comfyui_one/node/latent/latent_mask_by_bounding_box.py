from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	box: io.BoundingBoxes.Type
	device: tuple[str, int] | io.Combo.Type
	latent: io.Latent.Type
	value: tuple[str, int] | io.Float.Type

class OneLatentMaskByBoundingBox(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneLatentMaskByBoundingBox",
			display_name = "设置Latent噪波遮罩（边界框）",
			category = "One/模型/Latent",
			inputs = [
				io.Latent.Input(
					id = "latent",
					display_name = "Latent",
				),
				io.BoundingBoxes.Input(
					id = "box",
					display_name = "边界框",
				),
				io.Float.Input(
					id = "value",
					display_name = "数值",
					default = 1.0,
					min = 0.0,
					max = 1.0,
					raw_link = True,
					advanced = True,
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
				io.Latent.Output(
					id = "latent",
					display_name = "Latent",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		latent = kwargs["latent"]

		samples = latent["samples"]

		_, _, h, w = samples.shape

		device = kwargs["device"]

		graph = GraphBuilder()
		one_bounding_box_create_mask = graph.node(
			"OneBoundingBoxCreateMask",
			width = w,
			height = h,
			box = kwargs["box"],
			value = 1.0,
			device = device,
		)
		one_latent_mask = graph.node(
			"OneLatentMask",
			latent = latent,
			mask = one_bounding_box_create_mask.out(0),
			value = kwargs["value"],
			device = device,
		)

		return io.NodeOutput(
			one_latent_mask.out(0),
			expand = graph.finalize(),
		)
