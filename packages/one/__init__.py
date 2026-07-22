from comfy_api.latest import ComfyExtension, io
from nodes import EXTENSION_WEB_DIRS # type: ignore
# from pathlib import Path
from .node.bounding_box import (
	OneBoundingBox,
	OneBoundingBoxInspect,
)
from .node.execution import (
	OneExecutionBlock,
	OneExecutionVoid,
)
from .node.float import (
	OneFloat,
	OneFloatMax,
	OneFloatMin,
	OneFloatMultiply,
)
from .node.image import (
	OneImageCrop,
	OneImageCropByAlignment,
	OneImageCropByBoundingBox,
	OneImageGetHeight,
	OneImageGetLongerEdge,
	OneImageGetResolution,
	OneImageGetShorterEdge,
	OneImageGetSize,
	OneImageGetWidth,
	OneImageMatchColor,
	OneImagePadToMultiple,
	OneImageScale,
	OneImageScaleByEdge,
	OneImageStitch,
	OneImageTile,
)
from .node.int import (
	OneInt,
	OneIntMax,
	OneIntMin,
	OneIntMultiply,
)
from .node.latent import (
	OneLatentMask,
	OneLatentMaskByBoundingBox,
	OneLatentStitch,
)
from .node.mask import (
	OneMaskCreateBoundingBox,
	OneMaskGetSize,
	OneMaskMultiply,
	OneMaskPadToMultiple,
	OneMaskScale,
	OneMaskScaleByEdge,
)
from .node.list_select_by_index import OneListSelectByIndex

# EXTENSION_WEB_DIRS["one"] = Path(__file__).resolve().parent / "ui" / "dist"

class OneExtension(ComfyExtension):
	async def get_node_list(self) -> list[type[io.ComfyNode]]:
		return [
			OneBoundingBox,
			OneBoundingBoxInspect,
			OneExecutionBlock,
			OneExecutionVoid,
			OneFloat,
			OneFloatMax,
			OneFloatMin,
			OneFloatMultiply,
			OneImageCrop,
			OneImageCropByAlignment,
			OneImageCropByBoundingBox,
			OneImageGetHeight,
			OneImageGetLongerEdge,
			OneImageGetResolution,
			OneImageGetShorterEdge,
			OneImageGetSize,
			OneImageGetWidth,
			OneImageMatchColor,
			OneImagePadToMultiple,
			OneImageScale,
			OneImageScaleByEdge,
			OneImageStitch,
			OneImageTile,
			OneInt,
			OneIntMax,
			OneIntMin,
			OneIntMultiply,
			OneLatentMask,
			OneLatentMaskByBoundingBox,
			OneLatentStitch,
			OneListSelectByIndex,
			OneMaskCreateBoundingBox,
			OneMaskGetSize,
			OneMaskMultiply,
			OneMaskPadToMultiple,
			OneMaskScale,
			OneMaskScaleByEdge,
		]

async def comfy_entrypoint() -> ComfyExtension:
	return OneExtension()
