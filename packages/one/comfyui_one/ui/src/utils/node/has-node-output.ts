import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { find_node_output_index } from "./find-node-output-index";

export function has_node_output(node: LGraphNode, name: string): boolean {
	return 0 <= find_node_output_index(node, name);
}
