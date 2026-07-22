import {
	create_node_dom_widget,
	foreach_node_input_specification,
	transform_node_input_specification,
} from "../utils";
import { Number } from "../widgets";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Widget.Int",
	beforeRegisterNodeDef: (_, definition) => {
		foreach_node_input_specification(
			definition.input,
			(specification) => "INT" === specification.type,
			(_, specification) => {
				specification[0] = "ONE_INT";
			},
		);
	},
	getCustomWidgets: () => {
		return {
			ONE_INT: (node, name, data) => {
				const specification = transform_node_input_specification(name, data);
				const widget = create_node_dom_widget<number>(node, name, "one.int", specification, Number);

				return { widget };
			},
		};
	},
});
