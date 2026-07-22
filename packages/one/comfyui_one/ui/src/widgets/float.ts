import {
	create_node_dom_widget,
	foreach_node_input_specification,
	transform_node_input_specification,
} from "../internal/node";
import { Number } from "./components/number";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Widget.Float",
	beforeRegisterNodeDef: (_, definition) => {
		foreach_node_input_specification(
			definition.input,
			(specification) => "FLOAT" === specification.type,
			(_, specification) => {
				specification[0] = "ONE_FLOAT";
			},
		);
	},
	getCustomWidgets: () => {
		return {
			ONE_FLOAT: (node, name, data) => {
				const specification = transform_node_input_specification(name, data);
				const widget = create_node_dom_widget(node, name, "one.float", specification, Number);

				return { widget };
			},
		};
	},
});
