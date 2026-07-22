import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import { get_node_definition } from "./get-node-definition";

export function sort_node_inputs(node: LGraphNode): void {
	const input_order = get_node_definition(node)?.input_order;

	if (!input_order) {
		return;
	}

	const order = [...input_order.required ?? [], ...input_order.optional ?? []];

	node.inputs.sort((left, right) => {
		const left_index = order.indexOf(left.name.split("\x2E", 1)[0]!);
		const right_index = order.indexOf(right.name.split("\x2E", 1)[0]!);

		return (0 > left_index ? Infinity : left_index) - (0 > right_index ? Infinity : right_index);
	});
}
