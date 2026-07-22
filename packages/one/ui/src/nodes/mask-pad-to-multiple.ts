import { serialize } from "../internal/utils/common";
import { create_before_register_node_definition_hook as create_widget_combo_before_register_node_definition_hook } from "../widgets/combo";
import { app } from "@/scripts/app";

const TYPE = "OneMaskPadToMultiple";

app.registerExtension({
	name: `One.Node.${TYPE}`,

	beforeRegisterNodeDef: serialize(
		create_widget_combo_before_register_node_definition_hook(TYPE),
	),
});
