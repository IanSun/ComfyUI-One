from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	image: io.Image.Type

class OneImageGetSize(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageGetSize",
			display_name = "图像获取尺寸",
			category = "One/图像",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
				),
			],
			outputs = [
				io.Int.Output(
					id = "width",
					display_name = "宽度",
				),
				io.Int.Output(
					id = "height",
					display_name = "高度",
				),
				io.Int.Output(
					id = "longer",
					display_name = "长边",
				),
				io.Int.Output(
					id = "shorter",
					display_name = "短边",
				),
				io.Int.Output(
					id = "pixel",
					display_name = "像素",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		_, h, w, _ = kwargs["image"].shape

		return io.NodeOutput(
			w,
			h,
			max(h, w),
			min(h, w),
			h * w,
		)
