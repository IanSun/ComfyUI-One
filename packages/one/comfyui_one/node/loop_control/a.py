from collections import defaultdict, deque
from comfy_api.latest import io
from comfy_execution.graph_utils import GraphBuilder, is_link # type: ignore
from hashlib import md5
from typing import Unpack, cast
from .typing import OneLoopControlEndInputs, OneLoopControlStartInputs, OneLoopController

CHANNEL_SIZE = 10

T = { "a": 0 }

class OneLoopControlEnd(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneLoopControlEnd",
			display_name = "循环控制（结束）",
			category = "One/实用工具/控制",
			inputs = [
				OneLoopController.Input(
					id = "controller",
					display_name = "控制器",
					raw_link = True,
				),
				io.Boolean.Input(
					id = "condition",
					display_name = "条件",
					force_input = True,
				),
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
	def execute(cls, **kwargs: Unpack[OneLoopControlEndInputs]) -> io.NodeOutput:
		dynprompt = cls.hidden.dynprompt
		unique_id = cls.hidden.unique_id

		parts = unique_id.split(".", 2)
		if 2 < len(parts) and "OneLoopControl" == parts[0]:
			iteration = int(parts[1])
		else:
			iteration = 0

		print(f"==== OneLoopControlEnd({unique_id}) 迭代步数{T["a"]} ====")
		T["a"] = T["a"] + 1

		condition = kwargs.get("condition")
		if not condition or T["a"] > 3:
			outputs: set[int] = set()
			for id in dynprompt.all_node_ids():
				node = dynprompt.get_node(id)
				print(f"id: {id} inputs: {node["inputs"]}")
				for input in node["inputs"].values():
					if is_link(input) and unique_id == input[0]:
						outputs.add(input[1])

			# print(dynprompt.all_node_ids())
			# print(outputs)

			graph = GraphBuilder("")
			result: list[io.AnyType.Type | None] = []
			for index in range(CHANNEL_SIZE):
				link = cast(tuple[str, int] | None, kwargs.get(f"input.{index}"))
				if index in outputs:
					if link is not None:
						n = dynprompt.get_node(link[0])
						node = graph.node(n["class_type"], link[0]) # type: ignore
						for k, v in n["inputs"].items():
							node.set_input(k, v) # type: ignore
						result.append(node.out(link[1])) # type: ignore
						continue
	
				result.append(None)

			print(graph.finalize())

			return io.NodeOutput(*result, expand = graph.finalize())

		controller = kwargs.get("controller")
		print(f"controller: {controller[0]} unique_id: {unique_id}")

		def collect() -> list[str]:
			upstream: defaultdict[str, set[str]] = defaultdict(set)

			queue = deque([unique_id])
			while queue:
				id = queue.popleft()
				if controller[0] != id:
					node = dynprompt.get_node(id)
					print(f"-> 收集{id}上游 {node["inputs"]}")
					if "inputs" in node:
						for link in node["inputs"].values():
							if is_link(link):
								pid = link[0]
								if pid not in upstream:
									queue.append(pid)
								upstream[pid].add(id)
								print(f"    收集到上游{pid}")

			print(f"upstream: {upstream}")

			contained: set[str] = set()
			contained.add(controller[0])
			contained.add(unique_id)

			queue = deque([controller[0]])
			while queue:
				id = queue.popleft()
				for cid in upstream[id]:
					if cid not in contained:
						contained.add(cid)
						queue.append(cid)

			return list(contained)

		nodes = collect()
		print(f"依赖: {nodes}")

		def get_id(id: str) -> str:
			parts = id.split(".", 3)
			return parts[2] if 2 < len(parts) and "OneLoopControl" == parts[0] else id

		def get_iteration(id: str) -> int:
			parts = id.split(".", 2)
			return int(parts[1]) if 2 < len(parts) and "OneLoopControl" == parts[0] else 0

		iteration = get_iteration(controller[0])

		graph = GraphBuilder(f"OneLoopControl.{iteration + 1}.")

		for id in nodes:
			oid = get_id(id)
			n = dynprompt.get_node(id)
			node = graph.node(n["class_type"], oid) # type: ignore
			node.set_override_display_id(oid) # type: ignore
		print(f"初次构建图: {graph.finalize()}")
		for id in nodes:
			oid = get_id(id)
			n = dynprompt.get_node(id)
			print(f"-> 处理{n["class_type"]}({id})")
			node = graph.lookup_node(oid) # type: ignore
			for k, v in n["inputs"].items():
				print(f"    {k}: {v}")
				if is_link(v) and v[0] in nodes:
					parent = graph.lookup_node(v[0]) # type: ignore
					node.set_input(k, parent.out(v[1])) # type: ignore
				else:
					node.set_input(k, v) # type: ignore

		print(f"子图更新后：{graph.finalize()}")

		start, end = graph.lookup_node(controller[0]), graph.lookup_node(unique_id) # type: ignore

		for index in range(CHANNEL_SIZE):
			link = cast(tuple[str, int] | None, kwargs.get(f"input.{index}"))
			if link is not None:
				start.set_input(f"input.{index}", link) # type: ignore
				continue

			start.set_input(f"input.{index}", None) # type: ignore

		print(f"子图扩展后：{graph.finalize()}")

		result: list[io.AnyType.Type | None] = [
			end.out(index) # type: ignore
			for index in range(CHANNEL_SIZE)
		]

		return io.NodeOutput(*result, expand = graph.finalize())

	@classmethod
	def fingerprint_inputs(cls, **kwargs: Unpack[OneLoopControlStartInputs]) -> str:
		hash = md5()
		hash.update(str(kwargs.get("controller")).encode())
		hash.update(str(kwargs.get("condition")).encode())
		for index in range(CHANNEL_SIZE):
			link = cast(tuple[str, int] | None, kwargs.get(f"input.{index}"))
			hash.update(str(link).encode())

		return hash.hexdigest()

class OneLoopControlStart(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneLoopControlStart",
			display_name = "循环控制（开始）",
			category = "One/实用工具/控制",
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
				OneLoopController.Output(
					id = "controller",
					display_name = "控制器",
				),
				io.Int.Output(
					id = "iteration",
					display_name = "迭代步数",
				),
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
	def execute(cls, **kwargs: Unpack[OneLoopControlStartInputs]) -> io.NodeOutput:
		dynprompt = cls.hidden.dynprompt
		unique_id = cls.hidden.unique_id

		parts = unique_id.split(".", 2)
		if 2 < len(parts) and "OneLoopControl" == parts[0]:
			iteration = int(parts[1])
		else:
			iteration = 0

		outputs: set[int] = set()
		for id in dynprompt.all_node_ids():
			node = dynprompt.get_node(id)
			for input in node["inputs"].values():
				if is_link(input) and unique_id == input[0] and 0 < input[1]:
					outputs.add(input[1] - 2)

		graph = GraphBuilder(f"OneLoopControl.{iteration}.")
		result: list[io.AnyType.Type | None] = [None, iteration]
		for index in range(CHANNEL_SIZE):
			link = cast(tuple[str, int] | None, kwargs.get(f"input.{index}"))
			if index in outputs:
				if link is not None:
					n = dynprompt.get_node(link[0])
					node = graph.node(n["class_type"], link[0]) # type: ignore
					for k, v in n["inputs"].items():
						node.set_input(k, v) # type: ignore
					result.append(node.out(link[1])) # type: ignore
					continue

			result.append(None)

		return io.NodeOutput(*result, expand = graph.finalize())

	@classmethod
	def fingerprint_inputs(cls, **kwargs: Unpack[OneLoopControlStartInputs]) -> str:
		hash = md5()
		for index in range(CHANNEL_SIZE):
			link = cast(tuple[str, int] | None, kwargs.get(f"input.{index}"))
			hash.update(str(link).encode())

		return hash.hexdigest()
