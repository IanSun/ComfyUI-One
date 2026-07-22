import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { ISlotType } from "@comfyorg/graph-model/interfaces";

import { check_node_input_link } from "./check-node-input-link";
import { disconnect_node_input } from "./disconnect-node-input";
import { find_node_output_index } from "./find-node-output-index";
import { get_node_output_nodes_input } from "./get-node-output-nodes-input";

export const NODE_OUTPUT_TYPE_CACHE = new WeakMap<LGraphNode, Map<string, ISlotType>>();

export function set_node_output_type(node: LGraphNode, name: string, type: ISlotType): void {
	const index = find_node_output_index(node, name);
	if (0 > index) {
		return;
	}

	NODE_OUTPUT_TYPE_CACHE
		.getOrInsertComputed(node, () => new Map())
		.getOrInsertComputed(name, () => node.getOutputInfo(index)?.type ?? "*");
	node.setOutputDataType(index, type);

	for (const [input_node, input] of get_node_output_nodes_input(node, name)) {
		const input_name = input.name;
		if (!check_node_input_link(input_node, input_name)) {
			disconnect_node_input(input_node, input_name);
		}
	}

	node.setDirtyCanvas(true, true);
}
