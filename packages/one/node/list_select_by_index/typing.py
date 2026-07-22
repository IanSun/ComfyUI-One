from comfy_api.latest import io
from typing import TypedDict

class OneListSelectByIndexInputs(TypedDict):
	index: io.Int.Type
	input: io.AnyType.Type
