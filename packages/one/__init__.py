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
	OneExecutionSelect,
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

EXTENSION_WEB_DIRS["one"] = Path(__file__).resolve().parent / "ui" / "dist"

class OneExtension(ComfyExtension):
	async def get_node_list(self) -> list[type[io.ComfyNode]]:
		return [
			OneBoolean,
			OneBoundingBox,
			OneBoundingBoxInspect,
			OneExecutionBlock,
			OneExecutionFailover,
			OneExecutionSelect,
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
		]

async def comfy_entrypoint() -> ComfyExtension:
	return OneExtension()
