import {
	create_node_dom_widget,
	foreach_node_input_specification,
	transform_node_input_specification,
} from "../internal/node";
import { String } from "./components/string";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Widget.String",
	beforeRegisterNodeDef: (_, definition) => {
		foreach_node_input_specification(
			definition.input,
			(specification) => "STRING" === specification.type,
			(_, specification) => {
				specification[0] = "ONE_STRING";
			},
		);
	},
	getCustomWidgets: () => {
		return {
			ONE_STRING: (node, name, data) => {
				const specification = transform_node_input_specification(name, data);
				const widget = create_node_dom_widget(node, name, "one.string", specification, String);

				return { widget };
			},
		};
	},
});
