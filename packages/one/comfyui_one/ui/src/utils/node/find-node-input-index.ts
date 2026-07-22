import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

export function find_node_input_index(node: LGraphNode, name: string): number {
	return node.findInputSlot(name);
}
