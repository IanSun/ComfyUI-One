import { serialize } from "../internal/utils/common";
import { create_input_node_created_hook as create_widget_peer_node_created_hook } from "../widgets/peer";
import { app } from "@/scripts/app";

const TYPE = "OneExecutionSet";

app.registerExtension({
	name: `One.Node.${TYPE}`,

	nodeCreated: serialize(
		create_widget_peer_node_created_hook(TYPE, ["input", "name"]),
	),
});
