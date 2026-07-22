import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { find_node_input_index } from "./find-node-input-index";

export function has_node_input(node: LGraphNode, name: string): boolean {
	return 0 <= find_node_input_index(node, name);
}
