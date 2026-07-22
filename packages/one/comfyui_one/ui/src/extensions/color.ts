import {
	create_node_dom_widget,
	foreach_node_input_specification,
	transform_node_input_specification,
} from "../utils/node";
import { Color } from "../widgets";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Widget.Color",
	beforeRegisterNodeDef: (_, definition) => {
		foreach_node_input_specification(
			definition.input,
			(specification) => "COLOR" === specification.type,
			(_, specification) => {
				specification[0] = "ONE_COLOR";
			},
		);
	},
	getCustomWidgets: () => {
		return {
			ONE_COLOR: (node, name, data) => {
				const specification = transform_node_input_specification(name, data);
				const widget = create_node_dom_widget<string>(node, name, "one.color", specification, Color);

				return { widget };
			},
		};
	},
});
