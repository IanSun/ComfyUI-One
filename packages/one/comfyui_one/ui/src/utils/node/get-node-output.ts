import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { INodeOutputSlot } from "@comfyorg/graph-model/slots";

import { find_node_output_index } from "./find-node-output-index";

export function get_node_output(node: LGraphNode, name: string): INodeOutputSlot | undefined {
	const index = find_node_output_index(node, name);
	if (-1 < index) {
		return node.getOutputInfo(index) ?? undefined;
	}
}
