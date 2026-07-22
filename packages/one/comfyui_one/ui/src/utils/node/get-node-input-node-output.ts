import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { INodeOutputSlot } from "@comfyorg/graph-model/slots";

import { get_node_input_link } from "./get-node-input-link";
import { get_node_input_node } from "./get-node-input-node";

export function get_node_input_node_output(node: LGraphNode, name: string): [LGraphNode, INodeOutputSlot] | undefined {
	const link = get_node_input_link(node, name);
	if (!link) {
		return;
	}

	const output_node = get_node_input_node(node, name);
	if (!output_node) {
		return;
	}

	const output = output_node.getOutputInfo(link.origin_slot);
	if (output) {
		return [output_node, output];
	}
}
