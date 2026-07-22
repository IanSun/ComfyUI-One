import type { LGraphNode } from "@/lib/litegraph/src/litegraph";

import {
	get_node_cached_inputs,
	get_node_input_node_by_name,
	sync_node_inputs,
} from "@one/shared";
import { event_target } from "../shared";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Node.OneMultiplex",
	nodeCreated: (node) => {
		if ("OneMultiplex" !== node.comfyClass) {
			return;
		}

		const update_inputs = (): void => {
			const names: string[] = [];

			const pending: string[] = [];
			for (const { name } of get_node_cached_inputs(node)) {
				if (name.startsWith("input.")) {
					pending.push(name);

					if (get_node_input_node_by_name(node, name)) {
						names.push(...pending.splice(0));
					}
				}
				else {
					names.push(name);
				}
			}

			if (pending.length) {
				names.push(pending.shift()!);
			}

			sync_node_inputs(node, names);
		};

		node.onConnectionsChange = new Proxy(node.onConnectionsChange?.bind(node) ?? (() => {}), {
			apply: (target, thisArg, args: Parameters<NonNullable<LGraphNode["onConnectionsChange"]>>) => {
				switch (args[0]) {
					case 1: {
						update_inputs();
						break;
					}

					default:
				}

				event_target.dispatchEvent(new CustomEvent("One.Node.OneMultiplex:connection:change", { detail: node }));
				Reflect.apply(target, thisArg, args);
			},
		});

		update_inputs();
	},
});
