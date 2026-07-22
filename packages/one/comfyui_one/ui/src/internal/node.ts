import type { ISlotType } from "@/lib/litegraph/src/interfaces";
import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { LLink } from "@/lib/litegraph/src/LLink";
import type { INodeInputSlot, INodeOutputSlot } from "@/lib/litegraph/src/types/slots";
import type { IBaseWidget } from "@/lib/litegraph/src/types/widgets";
import type { InputSpec as InputSpecV2 } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef, InputSpec as InputSpecV1 } from "@/schemas/nodeDefSchema";
import type { DOMWidget } from "@/scripts/domWidget";
import type { LinkId } from "@/types";
import type { Atom } from "nanostores";
import type { FunctionComponent } from "react";

import { atom } from "nanostores";
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { serialize } from "./common";

export interface DOMWidgetProps<T, U = object> {
	definition: ComfyNodeDef;
	specification: InputSpecV2 & U;
	store: Atom<T | undefined>;

	/** @ts-expect-error */
	widget: DOMWidget<HTMLDivElement, T>;
}

const NODE_OUTPUT_TYPE_CACHE = new WeakMap<LGraphNode, Map<string, ISlotType>>();

export function add_node_input(node: LGraphNode, name: string, type: string, options?: Partial<INodeInputSlot>): void {
	if (!has_node_input(node, name)) {
		node.addInput(name, type, options);
	}
}

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

export function check_node_input_link(node: LGraphNode, name: string): boolean {
	const input = get_node_input(node, name);
	if (!input) {
		return false;
	}

	const node_output = get_node_input_node_output(node, name);
	return node_output ? node.canConnectTo(node_output[0], input, node_output[1]) : false;
}

export function create_node_dom_widget<T>(
	node: LGraphNode,
	name: string,
	type: string,
	specification: InputSpecV2,
	component: FunctionComponent<DOMWidgetProps<T>>,
): DOMWidgetProps<T>["widget"] | undefined {
	const definition = get_node_definition(node);
	if (!definition) {
		return;
	}

	const store = atom(specification.default as T | undefined);
	const element = document.createElement("div");

	/** @ts-expect-error */
	const widget = node.addDOMWidget<HTMLDivElement, T>(name, type, element, {
		getValue: () => {
			return store.get();
		},
		setValue: (value) => {
			store.set(value);
		},
	});
	widget.onRemove = serialize(
		widget.onRemove?.bind(widget),
		() => {
			root.unmount();
		},
	);

	const root = createRoot(element);
	root.render(
		createElement(component, {
			definition,
			specification,
			store,
			widget,
		}),
	);

	return widget;
}

export function disconnect_node_input(node: LGraphNode, name: string): void {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		node.disconnectInput(index);
	}
}

export function disconnect_node_output(node: LGraphNode, name: string): void {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		node.disconnectOutput(index);
	}
}

export function find_node_input_index(node: LGraphNode, name: string): number {
	return node.findInputSlot(name);
}

export function find_node_input_specification(
	input: ComfyNodeDef["input"],
	predicate: (specification: InputSpecV2, specification_1: InputSpecV1) => boolean,
): InputSpecV1 | undefined;
export function find_node_input_specification(
	input: ComfyNodeDef["input"],
	predicate: (specification: InputSpecV2, specification_1: InputSpecV1) => boolean,
	transform: true,
): InputSpecV2 | undefined;
export function find_node_input_specification(
	input: ComfyNodeDef["input"],
	predicate: (specification: InputSpecV2, specification_1: InputSpecV1) => boolean,
	transform?: true,
): InputSpecV1 | InputSpecV2 | undefined {
	for (const [index, record = {}] of [input?.required, input?.optional].entries()) {
		for (const [name, specification_1] of Object.entries(record)) {
			const specification = transform_node_input_specification(name, specification_1, 1 === index);

			if (predicate(specification, specification_1)) {
				return transform ? specification : specification_1;
			}
		}
	}
}

export function find_node_output_index(node: LGraphNode, name: string): number {
	return node.findOutputSlot(name);
}

export function foreach_node_input_specification(
	input: ComfyNodeDef["input"],
	predicate: (specification: InputSpecV2, specification_1: InputSpecV1) => boolean,
	callback: (specification: InputSpecV2, specification_1: InputSpecV1) => void,
): void {
	for (const [index, record = {}] of [input?.required, input?.optional].entries()) {
		for (const [name, specification_1] of Object.entries(record)) {
			const specification = transform_node_input_specification(name, specification_1, 1 === index);

			if (predicate(specification, specification_1)) {
				callback(specification, specification_1);
			}
		}
	}
}

export function get_node_definition(node: LGraphNode): ComfyNodeDef | undefined {
	return node.constructor.nodeData;
}

export function get_node_input(node: LGraphNode, name: string): INodeInputSlot | undefined {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		return node.getInputInfo(index) ?? undefined;
	}
}

export function get_node_input_link(node: LGraphNode, name: string): LLink | undefined {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		return node.getInputLink(index) ?? undefined;
	}
}

export function get_node_input_node(node: LGraphNode, name: string): LGraphNode | undefined {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		return node.getInputNode(index) ?? undefined;
	}
}

export function get_node_input_node_output(node: LGraphNode, name: string): [LGraphNode, INodeOutputSlot] | undefined {
	const link = get_node_input_link(node, name);
	if (!link) {
		return;
	}

	const output_node = get_node_input_node(node, name);
	if (!output_node) {
		return;
	}

	const output = output_node.getOutputInfo(link.origin_slot);
	if (output) {
		return [output_node, output];
	}
}

export function get_node_input_type(node: LGraphNode, name: string): ISlotType | undefined {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		return node.getInputDataType(index) ?? undefined;
	}
}

export function get_node_output(node: LGraphNode, name: string): INodeOutputSlot | undefined {
	const index = find_node_output_index(node, name);
	if (-1 < index) {
		return node.getOutputInfo(index) ?? undefined;
	}
}

export function get_node_output_links(node: LGraphNode, name: string): LLink[] {
	const links = new Map<LinkId, LLink>();
	for (const [input_node, input] of get_node_output_nodes_input(node, name)) {
		const link = get_node_input_link(input_node, input.name);
		if (link) {
			links.set(link.id, link);
		}
	}
	return links.values().toArray();
}

export function get_node_output_nodes(node: LGraphNode, name: string): LGraphNode[] {
	const index = find_node_output_index(node, name);
	return -1 < index ? node.getOutputNodes(index) ?? [] : [];
}

export function get_node_output_nodes_input(node: LGraphNode, name: string): [LGraphNode, INodeInputSlot][] {
	const node_id = node.id;
	const input_nodes = get_node_output_nodes(node, name);

	const nodes_input: [LGraphNode, INodeInputSlot][] = [];
	for (const input_node of input_nodes) {
		for (const input of input_node.inputs) {
			const node_output = get_node_input_node_output(input_node, input.name);

			if (node_id === node_output?.[0].id && name === node_output[1].name) {
				nodes_input.push([input_node, input]);
			}
		}
	}

	return nodes_input;
}

export function get_node_widget(node: LGraphNode, name: string): IBaseWidget | undefined {
	return node.widgets?.find((widget) => name === widget.name);
}

export function has_node_input(node: LGraphNode, name: string): boolean {
	return 0 <= find_node_input_index(node, name);
}

export function has_node_output(node: LGraphNode, name: string): boolean {
	return 0 <= find_node_output_index(node, name);
}

export function is_node_input_connected(node: LGraphNode, name: string): boolean {
	const index = find_node_input_index(node, name);
	return -1 < index && node.isInputConnected(index);
}

export function is_node_output_connected(node: LGraphNode, name: string): boolean {
	const index = find_node_output_index(node, name);
	return -1 < index && node.isOutputConnected(index);
}

export function remove_node_input(node: LGraphNode, name: string): void {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		node.removeInput(index);
	}
}

export function remove_node_output(node: LGraphNode, name: string): void {
	const index = find_node_output_index(node, name);
	if (-1 < index) {
		node.removeOutput(index);
	}
}

export function restore_node_output_type(node: LGraphNode, name: string): void {
	const index = find_node_output_index(node, name);
	if (0 > index) {
		return;
	}

	const cache = NODE_OUTPUT_TYPE_CACHE.get(node);
	if (!cache?.has(name)) {
		return;
	}

	const type = cache.get(name)!;
	node.setOutputDataType(index, type);

	for (const [input_node, input] of get_node_output_nodes_input(node, name)) {
		const input_name = input.name;
		if (!check_node_input_link(input_node, input_name)) {
			disconnect_node_input(input_node, input_name);
		}
	}

	node.setDirtyCanvas(true, true);
}

export function set_node_output_type(node: LGraphNode, name: string, type: ISlotType): void {
	const index = find_node_output_index(node, name);
	if (0 > index) {
		return;
	}

	NODE_OUTPUT_TYPE_CACHE
		.getOrInsertComputed(node, () => new Map())
		.getOrInsertComputed(name, () => node.getOutputInfo(index)?.type ?? "*");
	node.setOutputDataType(index, type);

	for (const [input_node, input] of get_node_output_nodes_input(node, name)) {
		const input_name = input.name;
		if (!check_node_input_link(input_node, input_name)) {
			disconnect_node_input(input_node, input_name);
		}
	}

	node.setDirtyCanvas(true, true);
}

export function sort_node_inputs(node: LGraphNode): void {
	const input_order = get_node_definition(node)?.input_order;

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

export function transform_node_input_specification(
	name: string,
	specification: InputSpecV1,
	optional = false,
): InputSpecV2 {
	return {
		isOptional: optional,
		name,
		type: ((type) => "string" === typeof type ? type : "UNKNOWN")(specification[0]),
		...specification[1],
	};
}

export function transform_node_input_specifications(input: ComfyNodeDef["input"]): InputSpecV2[] {
	return [input?.required, input?.optional].flatMap((record = {}, index) => {
		return Object.entries(record).map(([name, specification]) => {
			return transform_node_input_specification(name, specification, 1 === index);
		});
	});
}
