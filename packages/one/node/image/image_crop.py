from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	device: io.Combo.Type
	height: io.Int.Type
	image: io.Image.Type
	width: io.Int.Type
	x: io.Int.Type
	y: io.Int.Type

class OneImageCrop(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageCrop",
			display_name = "图像裁剪",
			category = "One/图像/变换",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
				),
				io.Int.Input(
					id = "x",
					display_name = "x",
					min = 0,
				),
				io.Int.Input(
					id = "y",
					display_name = "y",
					min = 0,
				),
				io.Int.Input(
					id = "width",
					display_name = "宽度",
					default = 1024,
					min = 0,
				),
				io.Int.Input(
					id = "height",
					display_name = "高度",
					default = 1024,
					min = 0,
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					display_name = "设备",
					advanced = True,
				),
			],
			outputs = [
				io.Image.Output(
					id = "image",
					display_name = "图像",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		image = kwargs["image"]

		_, h, w, _ = image.shape

		x, y = kwargs["x"], kwargs["y"]
		x1, x2 = min(w, x), min(w, x + kwargs["width"])
		y1, y2 = min(h, y), min(h, y + kwargs["height"])

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			image = image.to(device)

		if (0, 0, w, h) != (x1, y1, x2, y2):
			image = image[:, y1:y2, x1:x2, :].contiguous()

		return io.NodeOutput(image)
