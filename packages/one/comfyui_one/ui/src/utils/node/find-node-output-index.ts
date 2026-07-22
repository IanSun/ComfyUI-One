import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

export function find_node_output_index(node: LGraphNode, name: string): number {
	return node.findOutputSlot(name);
}
