# pyright: reportPrivateUsage=false

import torch
from abc import ABC, abstractmethod
from comfy_api.internal import _ComfyNodeInternal, _NodeOutputInternal
from comfy_execution.graph import DynamicPrompt
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, NotRequired, TypedDict

class _ComfyNodeBaseInternal(_ComfyNodeInternal):
	hidden: HiddenHolder | None = None

	...

class _ComfyType(ABC):
	io_type: str | None = None

	...

class _IO_V3:
	...

_Input = Input

_Output = Output

class _UIOutput(ABC):
	...

class AnyType(ComfyTypeIO):
	type Type = Any

class Autogrow(ComfyTypeI):
	type Type = dict[str, Any]

	_MaxNames = 100

	class _AutogrowTemplate:
		...

	class Input(ComfyTypeI.Input, DynamicInput):
		def __init__(
			self,
			id: str,
			template: Autogrow.TemplatePrefix | Autogrow.TemplateNames,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			extra_dict: dict[Any, Any] | None = None,
		) -> None:
			...

	class TemplateNames(_AutogrowTemplate):
		def __init__(
			self,
			input: Input,
			names: list[str],
			min: int = 1,
		) -> None:
			...

	class TemplatePrefix(_AutogrowTemplate):
		def __init__(
			self,
			input: Input,
			prefix: str,
			min: int = 1,
			max: int = 10,
		) -> None:
			...

		def as_dict(self) -> dict[str, Any]:
			...

	...

class Boolean(ComfyTypeIO):
	type Type = bool

	class Input(ComfyTypeIO.Input, WidgetInput):
		def __init__(
			self,
			id: str,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			default: bool | None = None,
			label_on: str | None = None,
			label_off: str | None = None,
			socketless: bool | None = None,
			force_input: bool | None = None,
			extra_dict: dict[Any, Any] | None = None,
			raw_link: bool | None = None,
			advanced: bool | None = None,
		) -> None:
			...

		...

class BoundingBox(ComfyTypeIO):
	class BoundingBoxDict(TypedDict):
		x: int
		y: int
		width: int
		height: int

	type Type = BoundingBoxDict

	class Input(ComfyTypeIO.Input, WidgetInput):
		def __init__(
			self,
			id: str,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			socketless: bool = True,
			default: BoundingBox.Type | None = None,
			component: str | None = None,
			force_input: bool | None = None,
		) -> None:
			...

		...

class BoundingBoxes(ComfyTypeIO):
	class BoundingBoxWithMetadata(BoundingBox.BoundingBoxDict):
		metadata: NotRequired[dict[Any, Any]]

	type Type = list[BoundingBoxWithMetadata]

	class Input(ComfyTypeIO.Input, WidgetInput):
		def __init__(
			self,
			id: str,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			socketless: bool = True,
			default: BoundingBoxes.Type | None = None,
			advanced: bool | None = None,
		) -> None:
			...

class Combo(ComfyTypeIO):
	type Type = str

	class Input(ComfyTypeIO.Input, WidgetInput):
		def __init__(
			self,
			id: str,
			options: list[str] | list[int] | type[Enum] | None = None,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			default: str | int | Enum | None = None,
			control_after_generate: bool | ControlAfterGenerate | None = None,
			upload: UploadType | None = None,
			image_folder: FolderType | None = None,
			remote: RemoteOptions | None = None,
			socketless: bool | None =None,
			extra_dict: dict[Any, Any] | None = None,
			raw_link: bool | None = None,
			advanced: bool | None = None,
		) -> None:
			...

		...

	class Output(ComfyTypeIO.Output):
		def __init__(
			self,
			id: str | None = None,
			display_name: str | None = None,
			options: list[str] | None = None,
			tooltip: str | None = None,
			is_output_list: bool = False,
		) -> None:
			...

class ComfyNode(_ComfyNodeBaseInternal):
	@classmethod
	def check_lazy_status(cls, **kwargs: Any) -> list[str]:
		...

	@classmethod
	@abstractmethod
	def define_schema(cls) -> Schema:
		...

	@classmethod
	@abstractmethod
	def execute(cls, **kwargs: Any) -> NodeOutput:
		...

	@classmethod
	def fingerprint_inputs(cls, **kwargs: Any) -> Any:
		...

	@classmethod
	def validate_inputs(cls, **kwargs: Any) -> bool | str:
		...

	...

class ComfyTypeI(_ComfyType):
	class Input(_Input):
		...

class ComfyTypeIO(ComfyTypeI):
	class Output(_Output):
		...

class ControlAfterGenerate(str, Enum):
	...

class DynamicInput(Input, ABC):
	...

class Float(ComfyTypeIO):
	type Type = float

	class Input(ComfyTypeIO.Input, WidgetInput):
		class GradientStop(TypedDict):
			color: tuple[int, int, int]
			offset: float

		def __init__(
			self,
			id: str,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			default: float | None = None,
			min: float | None = None,
			max: float | None = None,
			step: float | None = None,
			round: float | None = None,
			display_mode: NumberDisplay | None = None,
			gradient_stops: list[GradientStop] | None = None,
			socketless: bool | None = None,
			force_input: bool | None = None,
			extra_dict: dict[Any, Any] | None = None,
			raw_link: bool | None = None,
			advanced: bool | None = None,
		) -> None:
			...

		...

class FolderType(str, Enum):
	...

class Hidden(str, Enum):
	unique_id = ...
	prompt = ...
	extra_pnginfo = ...
	dynprompt = ...
	auth_token_comfy_org = ...
	api_key_comfy_org = ...
	comfy_usage_source = ...
	execution_list = ...

class HiddenHolder:
	unique_id: str
	prompt: Any
	extra_pnginfo: Any
	dynprompt: DynamicPrompt
	auth_token_comfy_org: str
	api_key_comfy_org: str
	comfy_usage_source: str
	execution_list: Any

class Image(ComfyTypeIO):
	type Type = torch.Tensor

class Input(_IO_V3):
	def __init__(
		self, id: str,
		display_name: str | None = None,
		optional: bool = False,
		tooltip: str | None = None,
		lazy: bool | None = None,
		extra_dict: dict[Any, Any] | None = None,
		raw_link: bool | None = None,
		advanced: bool | None = None,
	) -> None:
		...

	...

class Int(ComfyTypeIO):
	type Type = int

	class Input(ComfyTypeIO.Input, WidgetInput):
		def __init__(
			self,
			id: str,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			default: int | None = None,
			min: int | None = None,
			max: int | None = None,
			step: int | None = None,
			control_after_generate: bool | ControlAfterGenerate | None = None,
			display_mode: NumberDisplay | None = None,
			socketless: bool | None = None,
			force_input: bool | None = None,
			extra_dict: dict[Any, Any] | None = None,
			raw_link: bool | None = None,
			advanced: bool | None = None,
		) -> None:
			...

		...

class Latent(ComfyTypeIO):
	class LatentDict(TypedDict):
			samples: torch.Tensor
			noise_mask: NotRequired[torch.Tensor]
			batch_index: NotRequired[list[int]]
			type: NotRequired[str]

	type Type = LatentDict

class Mask(ComfyTypeIO):
	type Type = torch.Tensor

class MatchType(ComfyTypeIO):
	class Input(ComfyTypeIO.Input, _Input):
		def __init__(
			self,
			id: str,
			template: MatchType.Template,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			extra_dict: dict[Any, Any] | None = None,
			raw_link: bool | None = None,
			advanced: bool | None = None,
		) -> None:
			...

		...

	class Output(ComfyTypeIO.Output, _Output):
		def __init__(
			self,
			template: MatchType.Template,
			id: str | None = None,
			display_name: str | None = None,
			tooltip: str | None = None,
			is_output_list: bool = False,
		) -> None:
			...

		...

	class Template:
		def __init__(
			self,
			template_id: str,
			allowed_types: type[_ComfyType] | list[type[_ComfyType]] = AnyType,
		) -> None:
			...

		...

class MultiType:
	type Type = Any

	class Input(_Input):
		def __init__(
			self,
			id: str | Input,
			types: list[type[_ComfyType] | _ComfyType],
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			extra_dict: dict[Any, Any] | None = None,
			raw_link: bool | None = None,
			advanced: bool | None = None,
		) -> None:
			...

@dataclass
class NodeInfoV1:
	input: dict[str, dict[str, tuple[str, dict[str, Any]]]] | None = None
	input_order: dict[str, list[str]] | None = None
	is_input_list: bool | None = None
	output: list[str] | None = None
	output_is_list: list[bool] | None = None
	output_name: list[str] | None = None
	output_tooltips: list[str] | None = None
	output_matchtypes: list[str] | None = None
	name: str | None = None
	display_name: str | None = None
	description: str | None = None
	python_module: Any = None
	category: str | None = None
	output_node: bool | None = None
	deprecated: bool | None = None
	experimental: bool | None = None
	dev_only: bool | None = None
	api_node: bool | None = None
	search_aliases: list[str] | None = None
	essentials_category: str | None = None
	has_intermediate_output: bool | None = None

class NodeOutput(_NodeOutputInternal):
	def __init__(
		self,
		*args: Any,
		ui: _UIOutput | dict[Any, Any] | None = None,
		expand: dict[Any, Any] | None = None,
		block_execution: str | None = None,
	) -> None:
		...

	...

class NumberDisplay(str, Enum):
	...

class Output(_IO_V3):
	def __init__(
		self,
		id: str | None = None,
		display_name: str | None = None,
		tooltip: str | None = None,
		is_output_list: bool = False,
	) -> None:
		...

	...

@dataclass
class PriceBadge:
	expr: str
	depends_on: PriceBadgeDepends
	engine: str

	...

@dataclass
class PriceBadgeDepends:
	widgets: list[str]
	inputs: list[str]
	input_groups: list[str]

	...

class RemoteOptions:
	...

@dataclass
class Schema:
	node_id: str
	category: str
	display_name: str | None = None
	inputs: list[Input] = field(default_factory = list[Input])
	outputs: list[Output] = field(default_factory = list[Output])
	hidden: list[Hidden] = field(default_factory = list[Hidden])
	description: str = ...
	search_aliases: list[str] = field(default_factory = list[str])
	is_input_list: bool = False
	is_output_node: bool = False
	is_deprecated: bool = False
	is_experimental: bool = False
	is_dev_only: bool = False
	is_api_node: bool = False
	price_badge: PriceBadge | None = None
	not_idempotent: bool = False
	enable_expand: bool = False
	accept_all_inputs: bool = False
	essentials_category: str | None = None
	has_intermediate_output: bool = False

	def get_v1_info(self, cls: _ComfyNodeBaseInternal) -> NodeInfoV1:
		...

	...

class String(ComfyTypeIO):
	type Type = str

	class Input(ComfyTypeIO.Input, WidgetInput):
		def __init__(
			self,
			id: str,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			multiline: bool = False,
			placeholder: str | None = None,
			default: str | None = None,
			dynamic_prompts: bool | None = None,
			socketless: bool | None = None,
			force_input: bool | None = None,
			extra_dict: dict[Any, Any] | None = None,
			raw_link: bool | None = None,
			advanced: bool | None = None,
		) -> None:
			...

		...

class UploadType(str, Enum):
	...

class WidgetInput(Input):
	...

def comfytype[T](io_type: str) -> Callable[[type[T]], type[T]]:
	...

def finalize_prefix(prefix_list: list[str] | None, id: str | None = None) -> str:
	...


def get_dynamic_input_func(io_type: str) -> (
	Callable[[dict[str, Any], dict[str, Any], tuple[str, dict[str, Any]], str, list[str] | None], None] |
	None
):
	...

def register_dynamic_input_func(
	io_type: str,
	func: Callable[[dict[str, Any], dict[str, Any], tuple[str, dict[str, Any]], str, list[str] | None], None],
) -> None:
	...

...
