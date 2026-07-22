import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { find_node_output_index } from "./find-node-output-index";

export function remove_node_output(node: LGraphNode, name: string): void {
	const index = find_node_output_index(node, name);
	if (-1 < index) {
		node.removeOutput(index);
	}
}
