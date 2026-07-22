from comfy_api.latest import ComfyExtension, io
from importlib import import_module
from nodes import EXTENSION_WEB_DIRS # pyright: ignore[reportUnknownVariableType]
from pathlib import Path
from pkgutil import iter_modules

EXTENSION_WEB_DIRS["one"] = Path(__file__).resolve().parent / "ui" / "dist"

class OneExtension(ComfyExtension):
	async def get_node_list(self) -> list[type[io.ComfyNode]]:
		return [
			value
			for info in iter_modules(path = [str((Path(__file__).parent / "node").resolve())])
			for value in import_module(name=f".node.{info.name}", package=__package__).__dict__.values()
			if isinstance(value, type) and issubclass(value, io.ComfyNode)
		]

async def comfy_entrypoint() -> ComfyExtension:
	return OneExtension()
