import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { find_node_input_index } from "./find-node-input-index";

export function get_node_input_node(node: LGraphNode, name: string): LGraphNode | undefined {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		return node.getInputNode(index) ?? undefined;
	}
}
