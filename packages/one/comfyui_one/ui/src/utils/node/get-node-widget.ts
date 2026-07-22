import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { IBaseWidget } from "@comfyorg/graph-model/widgets";

export function get_node_widget(node: LGraphNode, name: string): IBaseWidget | undefined {
	return node.widgets?.find((widget) => name === widget.name);
}
