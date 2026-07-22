from comfy_api.latest import ComfyExtension, io
from nodes import EXTENSION_WEB_DIRS # pyright: ignore[reportUnknownVariableType]
from pathlib import Path
from .node.boolean import OneBoolean
from .node.bounding_box import (
	OneBoundingBox,
	OneBoundingBoxInspect,
)
from .node.execution import (
	OneExecutionBlock,
	OneExecutionFailover,
	OneExecutionGet,
	OneExecutionSelect,
	OneExecutionSet,
	OneExecutionSwitch,
	OneExecutionVoid,
)
from .node.float import (
	OneFloat,
	OneFloatAdd,
	OneFloatDivide,
	OneFloatExponentiate,
	OneFloatMax,
	OneFloatMin,
	OneFloatMultiply,
	OneFloatSubtract,
)
from .node.image import (
	OneImage,
	OneImageGetHeight,
	OneImageGetLongerEdge,
	OneImageGetResolution,
	OneImageGetShorterEdge,
	OneImageGetSize,
	OneImageGetWidth,
)
from .node.int import (
	OneInt,
	OneIntAdd,
	OneIntDivide,
	OneIntExponentiate,
	OneIntMax,
	OneIntMin,
	OneIntMultiply,
	OneIntSubtract,
)
from .node.mask import (
	OneMask,
	OneMaskGetHeight,
	OneMaskGetWidth,
)

EXTENSION_WEB_DIRS["one"] = Path(__file__).resolve().parent / "ui" / "dist"

class OneExtension(ComfyExtension):
	async def get_node_list(self) -> list[type[io.ComfyNode]]:
		return [
			OneBoolean,
			OneBoundingBox,
			OneBoundingBoxInspect,
			OneExecutionBlock,
			OneExecutionFailover,
			OneExecutionGet,
			OneExecutionSelect,
			OneExecutionSet,
			OneExecutionSwitch,
			OneExecutionVoid,
			OneFloat,
			OneFloatAdd,
			OneFloatDivide,
			OneFloatExponentiate,
			OneFloatMax,
			OneFloatMin,
			OneFloatMultiply,
			OneFloatSubtract,
			OneImage,
			OneImageGetHeight,
			OneImageGetLongerEdge,
			OneImageGetResolution,
			OneImageGetShorterEdge,
			OneImageGetSize,
			OneImageGetWidth,
			OneInt,
			OneIntAdd,
			OneIntDivide,
			OneIntExponentiate,
			OneIntMax,
			OneIntMin,
			OneIntMultiply,
			OneIntSubtract,
			OneMask,
			OneMaskGetHeight,
			OneMaskGetWidth,
		]

async def comfy_entrypoint() -> ComfyExtension:
	return OneExtension()
