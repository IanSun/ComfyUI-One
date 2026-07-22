from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack
from .image_crop import OneImageCrop

class OneImageCropByBoundingBoxInputs(TypedDict):
	box: io.BoundingBox.Type
	device: str
	image: Tensor

class OneImageCropByBoundingBox(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageCropByBoundingBox",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
				io.BoundingBox.Input(
					id = "box",
					default = {
						"x": 0,
						"y": 0,
						"width": 1024,
						"height": 1024,
					},
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					default = "default",
					advanced = True,
				),
			],
			outputs = [
				io.Image.Output(id = "image"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageCropByBoundingBoxInputs]) -> io.NodeOutput:
		box = kwargs["box"]

		return OneImageCrop.execute(
			image = kwargs["image"],
			x = box["x"],
			y = box["y"],
			width = box["width"],
			height = box["height"],
			device = kwargs["device"],
		)
