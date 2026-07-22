from typing import Any, TypedDict

class _NodeInfo(TypedDict):
	class_type: str
	inputs: dict[str, tuple[str, int]]

class DynamicPrompt:
	original_prompt: dict[str, _NodeInfo]
	node_overrides: dict[str, _NodeInfo]
	ephemeral_prompt: dict[str, _NodeInfo]
	ephemeral_parents: dict[str, str]
	ephemeral_display: dict[str, str]

	def get_node(self, node_id: str) -> _NodeInfo | None:
		...

	def override_node(self, node_id: str, node_info: _NodeInfo) -> None:
		...

	def has_node(self, node_id: str) -> bool:
		...

	def add_ephemeral_node(self, node_id: str, node_info: _NodeInfo, parent_id: str, display_id: str) -> None:
		...

	def get_real_node_id(self, node_id: str) -> str:
		...

	def get_parent_node_id(self, node_id: str) -> str | None:
		...

	def get_display_node_id(self, node_id: str) -> str:
		...

	def all_node_ids(self) -> set[str]:
		...

	def get_original_prompt(self) -> dict[str, Any]:
		...
