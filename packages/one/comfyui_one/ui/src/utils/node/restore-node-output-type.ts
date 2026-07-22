import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { check_node_input_link } from "./check-node-input-link";
import { disconnect_node_input } from "./disconnect-node-input";
import { find_node_output_index } from "./find-node-output-index";
import { get_node_output_nodes_input } from "./get-node-output-nodes-input";
import { NODE_OUTPUT_TYPE_CACHE } from "./set-node-output-type";

export function restore_node_output_type(node: LGraphNode, name: string): void {
	const index = find_node_output_index(node, name);
	if (0 > index) {
		return;
	}

	const cache = NODE_OUTPUT_TYPE_CACHE.get(node);
	if (!cache?.has(name)) {
		return;
	}

	const type = cache.get(name)!;
	node.setOutputDataType(index, type);

	for (const [input_node, input] of get_node_output_nodes_input(node, name)) {
		const input_name = input.name;
		if (!check_node_input_link(input_node, input_name)) {
			disconnect_node_input(input_node, input_name);
		}
	}

	node.setDirtyCanvas(true, true);
}
