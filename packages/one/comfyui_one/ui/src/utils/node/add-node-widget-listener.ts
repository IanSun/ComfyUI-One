import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { IBaseWidget } from "@comfyorg/graph-model/widgets";

import { serialize } from "../common";

export function add_node_widget_listener(node: LGraphNode, name: string, listener: (widget: IBaseWidget) => void): void {
	const { widgets } = node;

	const widget = widgets?.find((widget) => name === widget.name);

	if (!widget) {
		return;
	}

	widget.callback = serialize(
		widget.callback?.bind(widget),
		() => {
			Reflect.apply(listener, node, [widget]);
		},
	);
}
