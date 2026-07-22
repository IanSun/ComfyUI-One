import torch
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	device: io.Combo.Type
	mask: io.Mask.Type

class OneMaskCreateBoundingBox(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskCreateBoundingBox",
			display_name = "遮罩创建边界框",
			category = "One/图像/检测",
			inputs = [
				io.Mask.Input(
					id = "mask",
					display_name = "遮罩",
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					display_name = "设备",
					advanced = True,
				),
			],
			outputs = [
				io.BoundingBoxes.Output(
					id = "box",
					display_name = "边界框",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		mask = kwargs["mask"]

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			mask = mask.to(device)

		indices = torch.where(0 < mask)
		bi, yi, xi = indices[0].cpu(), indices[1].cpu(), indices[2].cpu()

		box: io.BoundingBoxes.Type = []
		for i in range(mask.shape[0]):
			mi = (bi == i)

			if mi.any().item():
				sy, sx = yi[mi], xi[mi]
				x1, x2, y1, y2 = (
					int(torch.min(sx).item()),
					int(torch.max(sx).item()),
					int(torch.min(sy).item()),
					int(torch.max(sy).item()),
				)

				box.append({
					"x": x1,
					"y": y1,
					"width": x2 - x1,
					"height": y2 - y1,
				})

			else:
				box.append({
					"x": 0,
					"y": 0,
					"width": 0,
					"height": 0,
				})

		return io.NodeOutput(box)
