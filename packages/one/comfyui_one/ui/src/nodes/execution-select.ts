import { serialize } from "../internal/utils/common";
import { create_before_register_node_definition_hook as create_widget_autogrow_before_register_node_definition_hook } from "../widgets/autogrow";
import {
	create_input_node_created_hook as create_widget_peer_input_node_created_hook,
	create_output_node_created_hook as create_widget_peer_output_node_created_hook,
} from "../widgets/peer";
import { app } from "@/scripts/app";

const TYPE = "OneExecutionSelect";

app.registerExtension({
	name: `One.Node.${TYPE}`,

	beforeRegisterNodeDef: serialize(
		create_widget_autogrow_before_register_node_definition_hook(TYPE),
	),

	nodeCreated: serialize(
		create_widget_peer_input_node_created_hook(TYPE, (node) => {
			const names = new Set<string>();

			for (const input of node.inputs) {
				const { name } = input;

				if (["index"].includes(name) || name.startsWith("input.")) {
					names.add(name);
				}
			}

			return [...names];
		}),
		create_widget_peer_output_node_created_hook(TYPE, (name, peer) => {
			const widget = peer.widgets?.find((widget) => "index" === widget.name);

			if (!widget) {
				return;
			}

			const { value } = widget;

			if ("number" !== typeof value || Number.isNaN(value)) {
				widget.value = 0;
				return;
			}

			const { length } = peer.inputs.filter((slot) => slot.name.startsWith("input."));
			const index = Math.max(0, Math.min(length - 1, value));

			if (value !== index) {
				widget.value = index;
			}

			const input = peer.getInputInfo(index);

			if (input) {
				return input.name;
			}
		}),
	),
});
