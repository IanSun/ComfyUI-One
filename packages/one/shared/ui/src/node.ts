import type { INodeInputSlot, INodeOutputSlot } from "@/lib/litegraph/src/interfaces";
import type { LGraphNode } from "@/lib/litegraph/src/LGraphNode";

const make_node_slot_comparator = (names: string[]) => {
	return <T extends INodeInputSlot | INodeOutputSlot>(x: T, y: T): number => {
		const [i, j] = [x, y].map(({ name }) => {
			const index = names.indexOf(name);
			return 0 > index ? Infinity : index;
		}) as [number, number];
		return i - j;
	};
};

const make_node_slot_name_predicator = (name: string) => {
	return (slot: INodeInputSlot | INodeOutputSlot): boolean => name === slot.name;
};

export const get_node_cached_input_by_name = (node: LGraphNode, name: string): INodeInputSlot | undefined => {
	const inputs = get_node_cached_inputs(node);
	return inputs.find(make_node_slot_name_predicator(name));
};

export const get_node_cached_inputs = (() => {
	const cache = new WeakMap<LGraphNode, INodeInputSlot[]>();

	return (node: LGraphNode): INodeInputSlot[] => {
		if (!cache.has(node)) {
			cache.set(node, [...node.inputs]);
		}
		return cache.get(node)!;
	};
})();

export const get_node_cached_output_by_name = (node: LGraphNode, name: string): INodeOutputSlot | undefined => {
	const outputs = get_node_cached_outputs(node);
	return outputs.find(make_node_slot_name_predicator(name));
};

export const get_node_cached_outputs = (() => {
	const cache = new WeakMap<LGraphNode, INodeOutputSlot[]>();

	return (node: LGraphNode): INodeOutputSlot[] => {
		if (!cache.has(node)) {
			cache.set(node, [...node.outputs]);
		}
		return cache.get(node)!;
	};
})();

export const get_node_input_by_name = (node: LGraphNode, name: string): INodeInputSlot | undefined => {
	return node.inputs.find(make_node_slot_name_predicator(name));
};

export const get_node_input_node_by_name = (node: LGraphNode, name: string): LGraphNode | undefined => {
	const slot = get_node_input_by_name(node, name);
	if (slot) {
		return node.getInputNode(node.inputs.indexOf(slot)) ?? undefined;
	}
};

export const get_node_input_nodes = (node: LGraphNode): LGraphNode[] => {
	return [
		...new Set(node.inputs.reduce<LGraphNode[]>((collection, _, index) => {
			const n = node.getInputNode(index);
			if (n) {
				collection.push(n);
			}
			return collection;
		}, [])),
	];
};

export const get_node_input_upstream_by_type = (node: LGraphNode, name: string, type: string): LGraphNode[] => {
	const collection = new Set<LGraphNode>();
	const pending = new Set<LGraphNode>();
	const n = get_node_input_node_by_name(node, name);
	if (n) {
		pending.add(n);
	}
	for (const n of pending) {
		if (type === n.type) {
			collection.add(n);
		}
		else {
			for (const u of get_node_input_nodes(n)) {
				pending.add(u);
			}
		}
	}
	return [...collection];
};

export const get_node_output_by_name = (node: LGraphNode, name: string): INodeOutputSlot | undefined => {
	return node.outputs.find(make_node_slot_name_predicator(name));
};

export const get_node_output_downstream_by_type = (node: LGraphNode, name: string, type: string): LGraphNode[] => {
	const collection = new Set<LGraphNode>();
	const pending = new Set<LGraphNode>(get_node_output_nodes_by_name(node, name));
	for (const n of pending) {
		if (type === n.type) {
			collection.add(n);
		}
		else {
			for (const d of get_node_output_nodes(n)) {
				pending.add(d);
			}
		}
	}
	return [...collection];
};

export const get_node_output_nodes = (node: LGraphNode): LGraphNode[] => {
	return [...new Set(node.outputs.flatMap((_, index) => node.getOutputNodes(index) ?? []))];
};

export const get_node_output_nodes_by_name = (node: LGraphNode, name: string): LGraphNode[] => {
	const slot = get_node_output_by_name(node, name);
	if (slot) {
		return node.getOutputNodes(node.outputs.indexOf(slot)) ?? [];
	}
	return [];
};

export const is_node_type = (node: LGraphNode, type: string): boolean => {
	return type === node.comfyClass;
};

export const make_node_slot_property_extractor = <T extends INodeInputSlot | INodeOutputSlot, P extends keyof T>(
	property: P,
) => (slot: T): T[P] => slot[property];

export const remove_node_input_by_name = (node: LGraphNode, name: string): INodeInputSlot | undefined => {
	const slot = get_node_input_by_name(node, name);
	if (slot) {
		void get_node_cached_inputs(node);
		node.removeInput(node.inputs.indexOf(slot));
	}
	return slot;
};

export const remove_node_output_by_name = (node: LGraphNode, name: string): INodeOutputSlot | undefined => {
	const slot = get_node_output_by_name(node, name);
	if (slot) {
		void get_node_cached_outputs(node);
		node.removeOutput(node.outputs.indexOf(slot));
	}
	return slot;
};

export const sort_node_inputs = (node: LGraphNode): INodeInputSlot[] => {
	return node.inputs.sort(
		make_node_slot_comparator(
			get_node_cached_inputs(node).map(make_node_slot_property_extractor("name")),
		),
	);
};

export const sort_node_outputs = (node: LGraphNode): INodeOutputSlot[] => {
	return node.outputs.sort(
		make_node_slot_comparator(
			get_node_cached_outputs(node).map(make_node_slot_property_extractor("name")),
		),
	);
};

export const sync_node_inputs = (node: LGraphNode, names: string[]): INodeInputSlot[] => {
	for (const input of get_node_cached_inputs(node)) {
		const { name } = input;
		if (names.includes(name)) {
			if (!node.inputs.some(make_node_slot_name_predicator(name))) {
				node.addInput(name, input.type, input);
			}
		}
		else {
			remove_node_input_by_name(node, name);
		}
	}
	return sort_node_inputs(node);
};

export const sync_node_outputs = (node: LGraphNode, names: string[]): INodeOutputSlot[] => {
	for (const output of get_node_cached_outputs(node)) {
		const { name } = output;
		if (names.includes(name)) {
			if (!node.outputs.some(make_node_slot_name_predicator(name))) {
				node.addOutput(name, output.type, output);
			}
		}
		else {
			remove_node_output_by_name(node, name);
		}
	}
	return sort_node_outputs(node);
};
