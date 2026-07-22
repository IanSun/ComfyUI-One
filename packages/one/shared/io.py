import builtins
from comfy_api.latest import io
from comfy_api.latest._io import (
	_ComfyNodeBaseInternal, # pyright: ignore[reportPrivateUsage]
	_ComfyType, # pyright: ignore[reportPrivateUsage]
	finalize_prefix,
	get_dynamic_input_func,
	register_dynamic_input_func,
)
# from enum import StrEnum
from typing import Any, Callable, TypedDict, cast

class OneAutogrow(io.Autogrow):
	class OneSchema:
		def get_v1_info(self, info: io.NodeInfoV1, cls: _ComfyNodeBaseInternal) -> None:
			input = info.input

			if input is None:
				return

			class NodeInfoV1InputDict(dict[str, tuple[str, dict[str, Any]]]):
				def __contains__(self, key: object) -> bool:
					if super().__contains__(key):
						return True

					if not isinstance(key, str):
						return False

					return self._resolve(key) is not None

				def __getitem__(self, key: Any) -> tuple[str, dict[str, Any]]:
					if super().__contains__(key):
						return super().__getitem__(key)

					if not isinstance(key, str):
						raise KeyError(key)

					value = self._resolve(key)

					if value is None:
						raise KeyError(key)

					return value

				def _resolve(self, key: str) -> tuple[str, dict[str, Any]] | None:
					io_type = OneAutogrow.io_type

					for name, specification in self.items():
						if not key.startswith(f"{name}."):
							continue

						if io_type != specification[0]:
							break

						spec = specification[1]
						template = spec["template"]
						s = key[len(name) + 1:]

						inner: tuple[str, dict[str, Any]] | None = None

						if "names" in template:
							if s in template["names"]:
								input = template["input"]
								inner = next(
									(
										group
										for category in input.values()
											for group in category.values()
									),
									None,
								)

						elif "prefix" in template:
							input = template["input"]
							inputs = cast(
								dict[str, tuple[str, dict[str, Any]]],
								{
									**input.get("optional", {}),
									**input.get("required", {}),
								}
							)

							if not inputs:
								break

							if 1 == len(inputs):
								prefix = template["prefix"]
								if s.startswith(prefix) and s[len(prefix):].isdigit():
									inner = next(iter(inputs.values()))
							else:
								for k, v in inputs.items():
									if s.startswith(k) and s[len(k):].isdigit():
										inner = v
										break

						if inner is None:
							break

						lazy = inner[1].get("lazy")
						if lazy is None:
							lazy = spec.get("lazy")

						if lazy is None:
							return inner

						return (
							inner[0],
							{
								**inner[1],
								"lazy": lazy,
							},
						)

			for key, value in input.items():
				input[key] = NodeInfoV1InputDict(value)

	class TemplatePrefix(io.Autogrow.TemplatePrefix):
		class OneOptions(TypedDict):
			max: int | None
			min: int

		overrides: OneOptions | None = None

		def __init__(
			self,
			input: io.Input,
			prefix: str,
			min: int = 0,
			max: int | None = None,
		) -> None:
			self.overrides = {
				"max": max,
				"min": min,
			}

			MaxNames = io.Autogrow._MaxNames

			min = builtins.min(MaxNames, min)
			max = builtins.max(1, builtins.min(MaxNames, min if max is None else max))

			super().__init__(
				input = input,
				prefix = prefix,
				min = min,
				max = max,
			)

		def as_dict(self) -> dict[str, Any]:
			return super().as_dict() | {
				"@one": self.overrides,
			}

	class Input(io.Autogrow.Input):
		class DynamicInputLookupProxy:
			def __init__(
				self,
				target: Callable[
					[dict[str, Any], dict[str, Any], tuple[str, dict[str, Any]], str, list[str] | None],
					None,
				],
			) -> None:
				self._target = target
	
			def __call__(
				self,
				out_dict: dict[str, Any],
				live_inputs: dict[str, Any],
				value: tuple[str, dict[str, Any]],
				input_type: str,
				curr_prefix: list[str] | None,
			) -> None:
				specification = value[1]
				template = specification["template"]
	
				if "@one" in template:
					if "prefix" in template:
						overrides = template["@one"]
						max = overrides["max"]
						min = overrides["min"]

						if max is None:
							prefix = finalize_prefix(curr_prefix, template["prefix"])
							offset = len(prefix)
							max = sum(
								1
								for key in live_inputs
								if key.startswith(prefix) and key[offset:].isdigit()
							)

						max = builtins.max(template["max"], min, max)

						value = (
							value[0],
							{
								**value[1],
								"template": {
									**template,
									"max": max,
								},
							},
						)
	
				return self._target(
					out_dict,
					live_inputs,
					value,
					input_type,
					curr_prefix,
				)

		def __init__(
			self,
			id: str,
			template: io.Autogrow.TemplatePrefix | io.Autogrow.TemplateNames,
			display_name: str | None = None,
			optional: bool = False,
			tooltip: str | None = None,
			lazy: bool | None = None,
			extra_dict: dict[Any, Any] | None = None,
		) -> None:
			io_type = OneAutogrow.io_type
			if io_type:
				expand_schema_for_dynamic = get_dynamic_input_func(io_type)
				if expand_schema_for_dynamic:
					if not isinstance(expand_schema_for_dynamic, OneAutogrow.Input.DynamicInputLookupProxy):
						register_dynamic_input_func(
							io_type,
							OneAutogrow.Input.DynamicInputLookupProxy(expand_schema_for_dynamic)
						)

			super().__init__(
				id = id,
				template = template,
				display_name = display_name,
				optional = optional,
				tooltip = tooltip,
				lazy = lazy,
				extra_dict = extra_dict,
			)

class OneSchema(io.Schema):
	EXTENSIONS: list[type[_ComfyType]] = [
		OneAutogrow,
	]

	def __getattribute__(self, name: str) -> Any:
		if name.startswith("_"):
			return super().__getattribute__(name)

		attr = super().__getattribute__(name)
		if not callable(attr):
			return attr

		if not callable(getattr(io.Schema, name, None)):
			return attr

		hooks: list[Callable[..., Any]] = []
		for extension in OneSchema.EXTENSIONS:
			hook = getattr(extension, "OneSchema", None)
			if hook is None:
				continue
			method = cast(Any, vars(hook)).get(name)
			if method is not None:
				hooks.append(method)

		if not hooks:
			return attr

		def proxy(*args: Any, **kwargs: Any) -> Any:
			result = attr(*args, **kwargs)
			for hook in hooks:
				hook(self, result, *args, **kwargs)
			return result

		return proxy
