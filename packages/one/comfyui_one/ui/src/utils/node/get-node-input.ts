import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { INodeInputSlot } from "@comfyorg/graph-model/slots";

import { find_node_input_index } from "./find-node-input-index";

export function get_node_input(node: LGraphNode, name: string): INodeInputSlot | undefined {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		return node.getInputInfo(index) ?? undefined;
	}
}
