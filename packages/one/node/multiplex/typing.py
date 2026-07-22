from comfy_api.latest import io
from typing import TypedDict

@io.comfytype(io_type="ONE_MULTIPLEX_STREAM") # type: ignore
class OneMultiplexStream:
	Type = list[tuple[str, int] | None]

	class Input(io.Input):
		pass

	class Output(io.Output):
		pass

class OneDemultiplexInputs(TypedDict):
	stream: OneMultiplexStream.Type

class OneMultiplexInputs(TypedDict):
	pass
