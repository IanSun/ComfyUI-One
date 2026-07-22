from comfy_api.latest import io
from typing import TypedDict, Unpack

class _Inputs(TypedDict):
	mask: io.Mask.Type

class OneMaskGetSize(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMaskGetSize",
			display_name = "遮罩获取尺寸",
			category = "One/图像/遮罩",
			inputs = [
				io.Mask.Input(
					id = "mask",
					display_name = "遮罩",
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
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		_, h, w = kwargs["mask"].shape

		return io.NodeOutput(
			w,
			h,
			max(h, w),
			min(h, w),
		)
