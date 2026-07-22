import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { INodeInputSlot } from "@comfyorg/graph-model/slots";

import { has_node_input } from "./has-node-input";

export function add_node_input(node: LGraphNode, name: string, type: string, options?: Partial<INodeInputSlot>): void {
	if (!has_node_input(node, name)) {
		node.addInput(name, type, options);
	}
}
