import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { LLink } from "@/lib/litegraph/src/LLink";

import { find_node_input_index } from "./find-node-input-index";

export function get_node_input_link(node: LGraphNode, name: string): LLink | undefined {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		return node.getInputLink(index) ?? undefined;
	}
}
