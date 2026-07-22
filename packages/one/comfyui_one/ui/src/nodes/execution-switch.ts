import { serialize } from "../internal/utils/common";
import {
	create_input_node_created_hook as create_widget_peer_input_node_created_hook,
	create_output_node_created_hook as create_widget_peer_output_node_created_hook,
} from "../widgets/peer";
import { app } from "@/scripts/app";

const TYPE = "OneExecutionSwitch";

app.registerExtension({
	name: `One.Node.${TYPE}`,

	nodeCreated: serialize(
		create_widget_peer_input_node_created_hook(TYPE, ["alternative", "input", "input_alternative"]),
		create_widget_peer_output_node_created_hook(TYPE, (name, peer) => {
			const widget = peer.widgets?.find((widget) => "alternative" === widget.name);

			if (!widget) {
				return;
			}

			const { value } = widget;

			if ("boolean" !== typeof value) {
				widget.value = false;
				return;
			}

			const index = peer.findInputSlot(value ? "input_alternative" : "input");
			if (0 > index) {
				return;
			}

			const input = peer.getInputInfo(index);

			if (input) {
				return input.name;
			}
		}),
	),
});
