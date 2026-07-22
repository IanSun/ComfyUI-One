import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { INodeInputSlot } from "@comfyorg/graph-model/slots";

import { get_node_input_node_output } from "./get-node-input-node-output";
import { get_node_output_nodes } from "./get-node-output-nodes";

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
