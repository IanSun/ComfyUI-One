import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { ComfyNodeDef } from "@comfyorg/object-info-parser";

export function get_node_definition(node: LGraphNode): ComfyNodeDef | undefined {
	return node.constructor.nodeData;
}
