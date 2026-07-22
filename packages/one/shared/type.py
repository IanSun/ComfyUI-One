from comfy_api.latest import io
from enum import StrEnum
from typing import Any

class Alignment(StrEnum):
	TopLeft = "左上对齐"
	Top = "上对齐"
	TopRight = "右上对齐"
	Left = "左对齐"
	Center = "中心对齐"
	Right = "右对齐"
	BottomLeft = "左下对齐"
	Bottom = "下对齐"
	BottomRight = "右下对齐"

class OneAlignment(io.Combo):
	Type = Alignment

	class Input(io.Combo.Input):
		def __init__(
			self,
			id: str,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			default: Alignment = Alignment.Center,
			socketless: bool | None = None,
			extra_dict: dict[Any, Any] | None = None,
			raw_link: bool | None = None,
			advanced: bool | None = None,
		):
			super().__init__(
				id = id,
				options = Alignment,
				display_name = display_name,
				optional = optional,
				tooltip = tooltip,
				lazy = lazy,
				default = default,
				socketless = socketless,
				extra_dict = extra_dict,
				raw_link = raw_link,
				advanced = advanced,
			)

		...
