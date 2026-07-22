from comfy_api.latest import io
from itertools import islice
from sys import maxsize
from typing import TypedDict, Unpack
from ...shared.io import OneAutogrow, OneSchema

class OneExecutionSelectInputs(TypedDict):
	index: int
	input: dict[str, tuple[str, int]]

class OneExecutionSelect(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return OneSchema(
			node_id = "OneExecutionSelect",
			category = "One/Execution",
			inputs = [
				OneAutogrow.Input(
					id = "input",
					template = OneAutogrow.TemplatePrefix(
						input = io.AnyType.Input(
							id = "input",
							raw_link = True,
						),
						prefix = "input",
						min = 0,
					),
					lazy = True,
				),
				io.Int.Input(
					id = "index",
					default = 0,
					min = 0,
					max = maxsize,
					step = 1,
				),
			],
			outputs = [
				io.AnyType.Output(id = "output"),
			],
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneExecutionSelectInputs]) -> io.NodeOutput:
		index = kwargs["index"]

		return io.NodeOutput(
			next(islice(kwargs["input"].values(), index, index + 1), None),
			expand = {},
		)

	@classmethod
	def check_lazy_status(cls, **kwargs: Unpack[OneExecutionSelectInputs]) -> list[str]:
		return []
