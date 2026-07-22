import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { find_node_output_index } from "./find-node-output-index";

export function get_node_output_nodes(node: LGraphNode, name: string): LGraphNode[] {
	const index = find_node_output_index(node, name);
	return -1 < index ? node.getOutputNodes(index) ?? [] : [];
}
