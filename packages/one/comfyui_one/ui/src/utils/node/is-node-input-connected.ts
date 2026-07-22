import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { find_node_input_index } from "./find-node-input-index";

export function is_node_input_connected(node: LGraphNode, name: string): boolean {
	const index = find_node_input_index(node, name);
	return -1 < index && node.isInputConnected(index);
}
