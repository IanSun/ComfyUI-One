import type { ISlotType } from "@/lib/litegraph/src/interfaces";
import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { ComfyExtension } from "@/types";

import { serialize } from "../internal/utils/common";
import { add_node_widget_listener } from "../internal/utils/node";
import { NodeSlotType } from "@/lib/litegraph/src/types/globalEnums";

const CACHE = new WeakMap<LGraphNode, Map<string, ISlotType>>();
const EVENT = "one.widget.peer:change";

export function create_input_node_created_hook(
	type: string,
	names: ((node: LGraphNode) => string[]) | string[],
): NonNullable<ComfyExtension["nodeCreated"]> {
	return (node) => {
		if (type !== node.comfyClass) {
			return;
		}

		const resolve_names = "function" === typeof names
			? names
			: (node: LGraphNode): string[] => node.inputs.map((slot) => slot.name);

		node.onConnectionsChange = serialize(
			node.onConnectionsChange?.bind(node),
			(type, index, connected, link, slot) => {
				if (NodeSlotType.INPUT !== type) {
					return;
				}

				const names = resolve_names(node);
				const input_name = slot.name;

				if (names.includes(input_name)) {
					dispatch_input_node_change_event(node);
				}
			},
		);

		const { widgets } = node;
		if (widgets) {
			const names = resolve_names(node);
			const state = { dirty: false };

			for (const widget of widgets) {
				const widget_name = widget.name;
				if (names.includes(widget_name)) {
					add_node_widget_listener(node, widget_name, () => {
						dispatch_input_node_change_event(node);
					});
					state.dirty = true;
				}
			}

			if (state.dirty) {
				requestIdleCallback(() => {
					dispatch_input_node_change_event(node);
				});
			}
		}
	};
}

export function create_output_node_created_hook(
	type: string,
	resolver: ((name: string, peer: LGraphNode, node: LGraphNode) => string | undefined) | [string, string],
): NonNullable<ComfyExtension["nodeCreated"]> {
	return (node) => {
		if (type !== node.comfyClass) {
			return;
		}

		const resolve = "function" === typeof resolver
			? resolver
			: (name: string): string | undefined => name === resolver[0] ? resolver[1] : undefined;

		const listener = (event: Event) => {
			const { detail: { node: peer } } = event as CustomEvent<{ node: LGraphNode }>;

			for (const [output_index, output] of node.outputs.entries()) {
				const output_name = output.name;
				const input_name = resolve(output_name, peer, node);

				if (input_name) {
					const input_index = peer.findInputSlot(input_name);
					if (-1 < input_index) {
						if (peer.isInputConnected(input_index)) {
							CACHE.getOrInsertComputed(node, () => new Map()).getOrInsert(output_name, output.type);

							const input_type = peer.getInputDataType(input_index) ?? "*";
							node.setOutputDataType(output_index, input_type);
							node.setDirtyCanvas(true, true);
						}
						else {
							const output_type = CACHE.get(node)?.get(output_name);
							if (output_type) {
								node.setOutputDataType(output_index, output_type);
								node.setDirtyCanvas(true, true);
							}
						}
					}
				}
			}
		};

		node.onRemoved = serialize(
			node.onRemoved?.bind(node),
			() => {
				globalThis.removeEventListener(EVENT, listener);
			},
		);

		globalThis.addEventListener(EVENT, listener);
	};
}

export function dispatch_input_node_change_event(node: LGraphNode): void {
	const event = new CustomEvent<{ node: LGraphNode }>(EVENT, { detail: { node } });
	globalThis.dispatchEvent(event);
}
