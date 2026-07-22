import { serialize } from "../internal/utils/common";
import { add_node_widget_listener } from "../internal/utils/node";
import {
	create_output_node_created_hook as create_widget_peer_node_created_hook,
	dispatch_input_node_change_event,
} from "../widgets/peer";
import { app } from "@/scripts/app";

const TYPE = "OneExecutionGet";
const PEER_TYPE = "OneExecutionSet";

app.registerExtension({
	name: `One.Node.${TYPE}`,

	nodeCreated: serialize(
		create_widget_peer_node_created_hook(TYPE, (name, peer, node) => {
			if (PEER_TYPE !== peer.type || "output" !== name) {
				return;
			}

			const widget = peer.widgets?.find((widget) => "name" === widget.name);
			return widget && widget.value === node.widgets?.find((widget) => "name" === widget.name)?.value ? "input" : undefined;
		}),
		(node) => {
			if (TYPE !== node.comfyClass) {
				return;
			}

			add_node_widget_listener(node, "name", (widget) => {
				const { value } = widget;

				const peer = node.graph?.nodes.find((node) => PEER_TYPE === node.comfyClass && value === node.widgets?.find((widget) => "name" === widget.name)?.value);
				if (peer) {
					dispatch_input_node_change_event(peer);
				}
			});
		},
	),
});
