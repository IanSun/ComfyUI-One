import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { find_node_input_index } from "./find-node-input-index";

export function remove_node_input(node: LGraphNode, name: string): void {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		node.removeInput(index);
	}
}
