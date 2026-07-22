import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { IBaseWidget } from "@/lib/litegraph/src/types/widgets";
import type { InputSpec as InputSpecV2 } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef, InputSpec as InputSpecV1 } from "@/schemas/nodeDefSchema";

import { serialize } from "./common";

export function add_node_widget_listener(node: LGraphNode, name: string, listener: (widget: IBaseWidget) => void): void {
	const { widgets } = node;

	const widget = widgets?.find((widget) => name === widget.name);

	if (!widget) {
		return;
	}

	widget.callback = serialize(
		widget.callback?.bind(widget),
		() => {
			Reflect.apply(listener, node, [widget]);
		},
	);
}

export function sort_node_inputs(node: LGraphNode): void {
	const input_order = node.constructor.nodeData?.input_order;

	if (!input_order) {
		return;
	}

	const order = [...input_order.required ?? [], ...input_order.optional ?? []];

	node.inputs.sort((left, right) => {
		const left_index = order.indexOf(left.name.split("\x2E", 1)[0]!);
		const right_index = order.indexOf(right.name.split("\x2E", 1)[0]!);

		return (0 > left_index ? Infinity : left_index) - (0 > right_index ? Infinity : right_index);
	});
}

export function transform_input_specification(
	name: string,
	specification: InputSpecV1,
	optional = false,
): InputSpecV2 {
	const options = {
		isOptional: optional,
		name,
		...specification[1],
	};

	const [type] = specification;

	if ("string" === typeof type) {
		return {
			type,
			...options,
		};
	}

	return {
		type: "UNKNOWN",
		...options,
	};
}

export function transform_input_specifications(input: ComfyNodeDef["input"]): InputSpecV2[] {
	return [input?.required, input?.optional].flatMap((record = {}, index) => {
		return Object.entries(record).map(([name, specification]) => {
			return transform_input_specification(name, specification, 1 === index);
		});
	});
}

export function transform_input_specifications_type<T extends ComfyNodeDef["input"]>(
	input: T,
	predicate: (specification: InputSpecV2) => boolean,
	callback: (specification: InputSpecV1) => void,
): T {
	for (const [index, record = {}] of [input?.required, input?.optional].entries()) {
		for (const [name, specification] of Object.entries(record)) {
			const s = transform_input_specification(name, specification, 1 === index);

			if (predicate(s)) {
				callback(specification);
			}
		}
	}

	return input;
}
