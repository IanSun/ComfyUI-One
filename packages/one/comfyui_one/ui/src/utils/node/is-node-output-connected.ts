import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { find_node_output_index } from "./find-node-output-index";

export function is_node_output_connected(node: LGraphNode, name: string): boolean {
	const index = find_node_output_index(node, name);
	return -1 < index && node.isOutputConnected(index);
}
