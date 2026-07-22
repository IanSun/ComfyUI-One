from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from sys import maxsize
from torch import Tensor, float32, tensor
from typing import NotRequired, TypedDict, Unpack, cast
from ..mask.mask import OneMask
from ..mask.mask_pad import OneMaskPad

class OneImagePadInputs(TypedDict):
	bottom: int
	color: str
	device: str
	image: Tensor
	left: int
	mask: NotRequired[Tensor]
	right: int
	top: int

class OneImagePad(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImagePad",
			category = "One/Image",
			inputs = [
				io.Image.Input(id = "image"),
				io.Mask.Input(
					id = "mask",
					optional = True,
				),
				io.Int.Input(
					id = "top",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "right",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "bottom",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Int.Input(
					id = "left",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
				io.Color.Input(
					id = "color",
					default = "#FFFFFF",
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
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneImagePadInputs]) -> io.NodeOutput:
		device = kwargs["device"]
		image = kwargs["image"]
		mask = kwargs.get("mask")

		image_shape = image.shape
		image_batch = image_shape[0]
		image_height = image_shape[1]
		image_width = image_shape[2]

		if mask is None:
			mask = cast(
				Tensor,
				OneMask.execute(
					width = image_width,
					height = image_height,
					value = 0.0,
					batch = image_batch,
					device = device,
				)[0],
			)

		mask_shape = mask.shape
		assert image_shape[:3] == mask_shape

		tensor_device = resolve_gpu_device_option(device)
		if tensor_device is not None:
			image = image.to(device = tensor_device)
			mask = mask.to(device = tensor_device)

		bottom = kwargs["bottom"]
		left = kwargs["left"]
		right = kwargs["right"]
		top = kwargs["top"]

		if 0 == bottom == left == right == top:
			return io.NodeOutput(
				image,
				mask,
			)

		color = kwargs["color"].lstrip("#")

		try:
			red, green, blue, *color_ = (value / 255.0 for value in bytes.fromhex(color))
			alpha = color_[0] if color_ else 1.0
		except ValueError:
			red, green, blue, alpha = 1.0, 1.0, 1.0, 1.0

		image_tensor = tensor(
			data = (red, green, blue),
			dtype = float32,
			device = tensor_device,
		)
		image_tensor = image_tensor.expand(image_batch, image_height + top + bottom, image_width + left + right, 3)
		image_tensor = image_tensor.clone()
		image_tensor[:, top:top + image_height, left:left + image_width, :] = image
		image = image_tensor

		mask = OneMaskPad.execute(
			mask = mask,
			top = top,
			right = right,
			bottom = bottom,
			left = left,
			value = 1.0 - alpha,
			device = device,
		)[0]

		return io.NodeOutput(
			image,
			mask,
		)
