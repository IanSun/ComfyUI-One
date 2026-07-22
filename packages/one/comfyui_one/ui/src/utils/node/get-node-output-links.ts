import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { LLink } from "@/lib/litegraph/src/LLink";
import type { LinkId } from "@/types";

import { get_node_input_link } from "./get-node-input-link";
import { get_node_output_nodes_input } from "./get-node-output-nodes-input";

export function get_node_output_links(node: LGraphNode, name: string): LLink[] {
	const links = new Map<LinkId, LLink>();
	for (const [input_node, input] of get_node_output_nodes_input(node, name)) {
		const link = get_node_input_link(input_node, input.name);
		if (link) {
			links.set(link.id, link);
		}
	}
	return links.values().toArray();
}
