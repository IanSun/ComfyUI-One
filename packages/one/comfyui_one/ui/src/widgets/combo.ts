import {
	create_node_dom_widget,
	foreach_node_input_specification,
	transform_node_input_specification,
} from "../internal/node";
import { Combo } from "./components/combo";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Widget.Combo",
	beforeRegisterNodeDef: (_, definition) => {
		foreach_node_input_specification(
			definition.input,
			(specification) => "COMBO" === specification.type,
			(_, specification) => {
				specification[0] = "ONE_COMBO";
			},
		);
	},
	getCustomWidgets: () => {
		return {
			ONE_COMBO: (node, name, data) => {
				const specification = transform_node_input_specification(name, data);
				const widget = create_node_dom_widget(node, name, "one.combo", specification, Combo);

				return { widget };
			},
		};
	},
});
