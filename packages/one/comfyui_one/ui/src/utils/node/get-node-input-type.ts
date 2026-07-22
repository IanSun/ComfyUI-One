import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { ISlotType } from "@comfyorg/graph-model/interfaces";

import { find_node_input_index } from "./find-node-input-index";

export function get_node_input_type(node: LGraphNode, name: string): ISlotType | undefined {
	const index = find_node_input_index(node, name);
	if (-1 < index) {
		return node.getInputDataType(index) ?? undefined;
	}
}
