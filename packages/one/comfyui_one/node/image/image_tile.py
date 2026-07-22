from comfy.model_management import get_gpu_device_options
from comfy_api.latest import io
from math import ceil
from sys import maxsize
from torch import Tensor
from typing import NotRequired, TypedDict, Unpack, cast
from ...shared.io import Alignment, OneAlignment
from .image_pad_to_size import OneImagePadToSize

class OneImageTileInputs(TypedDict):
	alignment: Alignment
	color: str
	device: str
	height: int
	image: Tensor
	mask: NotRequired[Tensor]
	overlap: int
	width: int

class OneImageTile(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageTile",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
				io.Mask.Input(
					id = "mask",
					optional = True,
				),
				io.Int.Input(
					id = "width",
					default = 1024,
					min = 1,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "height",
					default = 1024,
					min = 1,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "overlap",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				OneAlignment.Input(id = "alignment"),
				io.Color.Input(
					id = "color",
					default = "#FFFFFF",
					advanced = True,
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
				io.Mask.Output(id = "mask"),
				io.Int.Output(id = "row"),
				io.Int.Output(id = "column"),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImageTileInputs]) -> io.NodeOutput:
		height = kwargs["height"]
		overlap = kwargs["overlap"]
		width = kwargs["width"]

		overlap_height = min(overlap, height // 2)
		overlap_width = min(overlap, width // 2)

		step_height = height - overlap_height
		step_width = width - overlap_width

		image = kwargs["image"]

		image_shape = image.shape
		image_height = image_shape[1]
		image_width = image_shape[2]

		row = ceil((image_height - overlap_height) / step_height) if image_height > overlap_height else 1
		column = ceil((image_width - overlap_width) / step_width) if image_width > overlap_width else 1

		image, mask = cast(
			tuple[Tensor, Tensor],
			OneImagePadToSize.execute(
				image = image,
				**({
					"mask": kwargs["mask"],
				} if "mask" in kwargs else {}),
				width = step_width * (column - 1) + width,
				height = step_height * (row - 1) + height,
				alignment = kwargs["alignment"],
				color = kwargs["color"],
				device = kwargs["device"],
			),
		)

		image = (image
			.unfold(1, height, step_height)
			.unfold(2, width, step_width)
			.permute(0, 1, 2, 4, 5, 3)
			.flatten(0, 2)
		)

		mask = (mask
			.unfold(1, height, step_height)
			.unfold(2, width, step_width)
			.flatten(0, 2)
		)

		return io.NodeOutput(image, mask, row, column)
