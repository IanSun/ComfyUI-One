from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from torch import Tensor
from typing import TypedDict, Unpack
from .mask_crop import OneMaskCrop

class OneMaskCropByBoundingBoxInputs(TypedDict):
	box: io.BoundingBox.Type
	device: str
	mask: Tensor

class OneMaskCropByBoundingBox(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskCropByBoundingBox",
			category = "One/Mask",
			inputs = [
				io.Mask.Input(id = "mask"),
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
				io.Mask.Output(id = "mask"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMaskCropByBoundingBoxInputs]) -> io.NodeOutput:
		box = kwargs["box"]

		return OneMaskCrop.execute(
			mask = kwargs["mask"],
			x = box["x"],
			y = box["y"],
			width = box["width"],
			height = box["height"],
			device = kwargs["device"],
		)
