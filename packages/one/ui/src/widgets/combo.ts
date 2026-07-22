import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { zComboInputOptions } from "@/schemas/nodeDefSchema";
import type { ComfyApp } from "@/scripts/app";
import type { ComfyExtension } from "@/types";
import type z from "zod";

import {
	transform_input_specification,
	transform_input_specifications_type,
} from "../internal/utils/node";
import zh from "../locales/zh/nodeDefs.json";
import { app } from "@/scripts/app";

type ComboSpecification = z.infer<typeof zComboInputOptions>;

const MESSAGE: Record<
	string,
	Record<
		string,
		{
			inputs?: Record<string, unknown>;
		}
	>
> = {
	zh,
};

export function create_before_register_node_definition_hook(
	type: string,
): NonNullable<ComfyExtension["beforeRegisterNodeDef"]> {
	return (_, definition) => {
		if (type !== definition.name) {
			return;
		}

		transform_input_specifications_type(
			definition.input,
			(specification) => {
				return "COMBO" === specification.type;
			},
			(specification) => {
				specification[0] = "ONE_COMBO";
			},
		);
	};
}

function resolve_combo_option_localized_name(node: LGraphNode, app: ComfyApp, name: string, key: string): string {
	const locale = app.extensionManager.setting.get("Comfy.Locale") as string;
	const messages = (MESSAGE[locale]?.[node.constructor.nodeData!.name]?.inputs?.[name] ?? {}) as {
		name?: string;
		options?: Record<string, string>;
	};

	const localized_name = messages.options?.[key] ?? key;

	return localized_name;
}

app.registerExtension({
	name: "One.Widget.Combo",
	getCustomWidgets: () => {
		return {
			ONE_COMBO: (node, name, data, app) => {
				const specification = transform_input_specification(name, data) as unknown as ComboSpecification;

				const widget = node.addWidget(
					"combo",
					name,
					specification.default ?? specification.options?.[0] ?? "",
					() => {},
					{
						values: specification.options ?? [],
						getOptionLabel: (value) => {
							return value ? resolve_combo_option_localized_name(node, app, name, value) : "";
						},
					},
				);

				return { widget };
			},
		};
	},
});
