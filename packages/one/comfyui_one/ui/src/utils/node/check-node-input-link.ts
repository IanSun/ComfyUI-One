import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { get_node_input } from "./get-node-input";
import { get_node_input_node_output } from "./get-node-input-node-output";

export function check_node_input_link(node: LGraphNode, name: string): boolean {
	const input = get_node_input(node, name);
	if (!input) {
		return false;
	}

	const node_output = get_node_input_node_output(node, name);
	return node_output ? node.canConnectTo(node_output[0], input, node_output[1]) : false;
}
