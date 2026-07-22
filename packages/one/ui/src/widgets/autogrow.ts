import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { zAutogrowOptions } from "@/schemas/nodeDefSchema";
import type { ComfyApp } from "@/scripts/app";
import type { ComfyExtension } from "@/types";
import type z from "zod";

import { serialize } from "../internal/utils/common";
import {
	transform_input_specification,
	transform_input_specifications,
	transform_input_specifications_type,
} from "../internal/utils/node";
import zh from "../locales/zh/nodeDefs.json";
import { NodeSlotType, RenderShape } from "@/lib/litegraph/src/types/globalEnums";
import { app } from "@/scripts/app";

type AutogrowNode = {
	comfyDynamic: {
		"one.autogrow": Record<
			string,
			{
				input: InputSpec[];
				max: number;
				min: number;
				names?: string[];
				prefix?: string;
			}
		>;
	};
} & LGraphNode;
type AutogrowSpecification = {
	template: {
		"@one"?: {
			max?: number;
		};
	};
} & z.infer<typeof zAutogrowOptions>;

const MESSAGE: Record<
	string,
	Record<
		string,
		{
			inputs?: Record<string, unknown>;
		}
	>
> = {
	zh,
};

export function create_before_register_node_definition_hook(
	type: string,
): NonNullable<ComfyExtension["beforeRegisterNodeDef"]> {
	return (_, definition) => {
		if (type !== definition.name) {
			return;
		}

		transform_input_specifications_type(
			definition.input,
			(specification) => {
				return "COMFY_AUTOGROW_V3" === specification.type;
			},
			(specification) => {
				specification[0] = "ONE_AUTOGROW";
			},
		);
	};
}

function add_autogrow_group(node: AutogrowNode, app: ComfyApp, name: string, index: number, map: Map<string, number>): void {
	const { input, max, min } = node.comfyDynamic["one.autogrow"][name]!;

	if (max <= index) {
		return;
	}

	const slots = node.inputs;

	for (const i of input) {
		const n = resolve_autogrow_input_name(node, name, i.name, index);

		if (slots.every(({ name }) => n !== name)) {
			node.addInput(
				n,
				i.type,
				{
					localized_name: resolve_autogrow_input_localized_name(node, app, name, i.name, index),
					...(index >= min || i.isOptional) && { shape: RenderShape.HollowCircle },
				},
			);
		}

		map.set(n, index);
	}
}

function add_autogrow_listeners(node: AutogrowNode, app: ComfyApp, name: string, map: Map<string, number>): void {
	node.onConnectionsChange = serialize(
		node.onConnectionsChange?.bind(node),
		(type, _, connected, link, slot) => {
			if (NodeSlotType.INPUT !== type) {
				return;
			}

			if (connected) {
				if (link) {
					const index = map.get(slot.name);

					if (Math.max(0, ...map.values()) === index) {
						add_autogrow_group(node, app, name, index + 1, map);
					}
				}

				return;
			}

			const { inputs } = node;

			const slots = inputs
				.filter(({ name }) => map.has(name))
				.sort(({ name: left }, { name: right }) => map.get(right)! - map.get(left)!);

			const indexes = new Set<number>();
			for (const slot of slots) {
				const index = map.get(slot.name)!;

				if (node.isInputConnected(inputs.indexOf(slot))) {
					indexes.delete(index);
					break;
				}

				indexes.add(index);
			}

			for (const index of indexes) {
				remove_autogrow_group(node, name, index, map);
			}

			if (0 < indexes.size) {
				add_autogrow_group(node, app, name, 0 < map.size ? Math.max(...map.values()) + 1 : 0, map);
			}
		},
	);
}

function remove_autogrow_group(node: AutogrowNode, name: string, index: number, map: Map<string, number>): void {
	const { input, min } = node.comfyDynamic["one.autogrow"][name]!;

	if (min > index) {
		return;
	}

	const slots = node.inputs;

	for (const i of input) {
		const n = resolve_autogrow_input_name(node, name, i.name, index);
		const slot = slots.findIndex((slot) => n === slot.name);

		if (-1 < slot) {
			node.removeInput(slot);
			map.delete(n);
		}
	}
}

function resolve_autogrow_input_localized_name(node: AutogrowNode, app: ComfyApp, name: string, key: string, index: number): string {
	const locale = app.extensionManager.setting.get("Comfy.Locale") as string;
	const messages = (MESSAGE[locale]?.[node.constructor.nodeData!.name]?.inputs?.[name] ?? {}) as {
		name?: string;
		template?: {
			names?: string[];
			prefix?: string;
		};
	};

	const { input, names, prefix = "" } = node.comfyDynamic["one.autogrow"][name]!;
	const localized_name = names
		? messages.template?.names?.[index] ?? names[index]!
		: (1 === input.length ? messages.template?.prefix ?? prefix : messages.name ?? key) + index;

	return localized_name;
}

function resolve_autogrow_input_name(node: AutogrowNode, name: string, key: string, index: number): string {
	const { input, names, prefix = "" } = node.comfyDynamic["one.autogrow"][name]!;
	const display_name = names ? names[index]! : (1 === input.length ? prefix : key) + index;

	return `${name}.${display_name}`;
}

app.registerExtension({
	name: "One.Widget.Autogrow",
	getCustomWidgets: () => {
		return {
			ONE_AUTOGROW: (node, name, data, app) => {
				const specification = transform_input_specification(name, data) as unknown as AutogrowSpecification;
				const { "@one": { max } = {}, input, min = 0, names, prefix } = specification.template;

				const options = {
					input: transform_input_specifications(input),
					max: names?.length ?? Math.max(min, max ?? Infinity),
					min,
					names,
					prefix,
				};

				Reflect.set(
					(node.comfyDynamic ??= {})["one.autogrow"] ??= {},
					name,
					options,
				);

				const slot = node.inputs.findIndex((slot) => name === slot.name);
				if (-1 < slot) {
					node.removeInput(slot);
				}

				const map = new Map<string, number>();

				for (let index = 0; 0 === index || options.min + 1 > index; index += 1) {
					add_autogrow_group(node as AutogrowNode, app, name, index, map);
				}

				add_autogrow_listeners(node as AutogrowNode, app, name, map);

				return {};
			},
		};
	},
});
