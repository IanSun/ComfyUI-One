from comfy_api.latest import ComfyExtension, io
from nodes import EXTENSION_WEB_DIRS # type: ignore
# from pathlib import Path
from .node.bounding_box import (
	OneBoundingBox,
	OneBoundingBoxCreateMask,
	OneBoundingBoxGetProperty,
	OneBoundingBoxScale,
)
from .node.execution_block import OneExecutionBlock
from .node.image import (
	OneImageCrop,
	OneImageCropByAlignment,
	OneImageCropByBoundingBox,
	OneImageGetSize,
	OneImageMatchColor,
	OneImagePadToMultiple,
	OneImageScale,
	OneImageScaleByEdge,
	OneImageStitch,
	OneImageTile,
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
from .node.multiplex import OneDemultiplex, OneMultiplex

# EXTENSION_WEB_DIRS["one"] = Path(__file__).resolve().parent / "ui" / "dist"

class OneExtension(ComfyExtension):
	async def get_node_list(self) -> list[type[io.ComfyNode]]:
		return [
			OneBoundingBox,
			OneBoundingBoxCreateMask,
			OneBoundingBoxGetProperty,
			OneBoundingBoxScale,
			OneDemultiplex,
			OneExecutionBlock,
			OneImageCrop,
			OneImageCropByAlignment,
			OneImageCropByBoundingBox,
			OneImageGetSize,
			OneImageMatchColor,
			OneImagePadToMultiple,
			OneImageScale,
			OneImageScaleByEdge,
			OneImageStitch,
			OneImageTile,
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
			OneMultiplex,
		]

async def comfy_entrypoint() -> ComfyExtension:
	return OneExtension()
