import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import {
	get_node_cached_outputs,
	get_node_input_upstream_by_type,
	make_node_slot_property_extractor,
	sync_node_outputs,
} from "@one/shared";
import { event_target } from "../shared";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Node.OneDemultiplex",
	nodeCreated: (node) => {
		if ("OneDemultiplex" !== node.comfyClass) {
			return;
		}

		const update_outputs = (): void => {
			const prefix = "输出";

			const outputs = get_node_cached_outputs(node);
			const n = outputs.find((output) => output.name.startsWith(prefix))?.name;

			const upstream = get_node_input_upstream_by_type(node, "stream", "OneMultiplex");
			const names = [
				...new Set(
					upstream.flatMap((node) => node.inputs.map(make_node_slot_property_extractor("name"))),
				),
			]
				.map((name) => name.replace("input.", prefix));

			if (n && !names.includes(n)) {
				names.push(n);
			}

			sync_node_outputs(node, names);
		};

		node.onConnectionsChange = new Proxy(node.onConnectionsChange?.bind(node) ?? (() => {}), {
			apply: (target, thisArg, args: Parameters<NonNullable<LGraphNode["onConnectionsChange"]>>) => {
				switch (args[0]) {
					case 1: {
						update_outputs();
						break;
					}

					default:
				}

				Reflect.apply(target, thisArg, args);
			},
		});

		event_target.addEventListener("One.Node.OneMultiplex:connection:change", () => {
			update_outputs();
		});

		update_outputs();
	},
});
