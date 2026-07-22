from comfy_api.latest import io
from typing import TypedDict

@io.comfytype(io_type="ONE_LOOP_CONTROLLER") # type: ignore
class OneLoopController:
	Type = None

	class Input(io.Input):
		pass

	class Output(io.Output):
		pass

class OneLoopControlStartInputs(TypedDict):
	pass

class OneLoopControlEndInputs(TypedDict):
	controller: tuple[str, int]
	condition: io.Boolean.Type
