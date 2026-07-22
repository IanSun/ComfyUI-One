from comfy_api.latest import io
from comfy_execution.graph_utils import is_link # type: ignore
from os import urandom
from typing import Unpack, cast
from .typing import OneDemultiplexInputs, OneMultiplexInputs, OneMultiplexStream

CHANNEL_SIZE = 10

class OneDemultiplex(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneDemultiplex",
			display_name = "多路解复用",
			category = "One/实用工具",
			inputs = [
				OneMultiplexStream.Input(
					id = "stream",
					display_name = "流",
				),
			],
			outputs = [
				*[
					io.AnyType.Output(
						id = f"output.{i}",
						display_name = f"输出{i}",
					)
					for i in range(CHANNEL_SIZE)
				],
			],
			hidden = [
				io.Hidden.dynprompt,
				io.Hidden.unique_id,
			],
			enable_expand = True,
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneDemultiplexInputs]) -> io.NodeOutput:
		dynprompt = cls.hidden.dynprompt
		unique_id = cls.hidden.unique_id

		stream = kwargs.get("stream")

		outputs: set[int] = set()
		for id in dynprompt.all_node_ids():
			node = dynprompt.get_node(id)
			for input in node["inputs"].values():
				if is_link(input) and unique_id == input[0]:
					outputs.add(input[1])

		result: list[io.AnyType.Type | None] = [
			link if index in outputs else None
			for index, link in enumerate(stream)
		]

		return io.NodeOutput(*result, expand = {})

	@classmethod
	def fingerprint_inputs(cls, **kwargs: Unpack[OneDemultiplexInputs]) -> str:
		return urandom(16).hex()

class OneMultiplex(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneMultiplex",
			display_name = "多路复用",
			category = "One/实用工具",
			inputs = [
				*[
					io.AnyType.Input(
						id = f"input.{i}",
						display_name = f"输入{i}",
						optional = True,
						lazy = True,
						raw_link = True,
					)
					for i in range(CHANNEL_SIZE)
				],
			],
			outputs = [
				OneMultiplexStream.Output(
					id = "stream",
					display_name = "流",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[OneMultiplexInputs]) -> io.NodeOutput:
		stream: list[tuple[str, int] | None] = []
		for index in range(CHANNEL_SIZE):
			stream.append(cast(tuple[str, int] | None, kwargs.get(f"input.{index}")))

		return io.NodeOutput(stream)
