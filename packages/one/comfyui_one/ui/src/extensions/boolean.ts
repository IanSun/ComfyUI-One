import {
	create_node_dom_widget,
	foreach_node_input_specification,
	transform_node_input_specification,
} from "../utils";
import { Boolean } from "../widgets";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Widget.Boolean",
	beforeRegisterNodeDef: (_, definition) => {
		foreach_node_input_specification(
			definition.input,
			(specification) => "BOOLEAN" === specification.type,
			(_, specification) => {
				specification[0] = "ONE_BOOLEAN";
			},
		);
	},
	getCustomWidgets: () => {
		return {
			ONE_BOOLEAN: (node, name, data) => {
				const specification = transform_node_input_specification(name, data);
				const widget = create_node_dom_widget<boolean>(node, name, "one.boolean", specification, Boolean);

				return { widget };
			},
		};
	},
});
