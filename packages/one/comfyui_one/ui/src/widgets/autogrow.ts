import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { zAutogrowOptions } from "@/schemas/nodeDefSchema";
import type z from "zod";

import i18next from "i18next";
import { serialize } from "../internal/common";
import {
	add_node_input,
	foreach_node_input_specification,
	get_node_definition,
	is_node_input_connected,
	remove_node_input,
	sort_node_inputs,
	transform_node_input_specification,
	transform_node_input_specifications,
} from "../internal/node";
import { create_node_input_translation } from "./utils/i18n";
import { NodeSlotType, RenderShape } from "@/lib/litegraph/src/types/globalEnums";
import { app } from "@/scripts/app";

type InputAutogrowSpecification = {
	template: { input: InputSpec[] }
		& Omit<z.infer<typeof zAutogrowOptions>["template"], "max" | "min">
		& Required<Pick<z.infer<typeof zAutogrowOptions>["template"], "max" | "min">>;
} & InputSpec & Omit<z.infer<typeof zAutogrowOptions>, "template">;

function add_autogrow_input_group(node: LGraphNode, specification: InputAutogrowSpecification, index: number): void {
	const {
		input,
		max,
		min,
	} = specification.template;

	if (max <= index) {
		return;
	}

	for (const spec of input) {
		const resolved = resolve_autogrow_input_name(node, specification, input, spec, index);
		if (!resolved) {
			continue;
		}

		const { localized_name, name } = resolved;

		add_node_input(node, name, spec.type, {
			localized_name,
			...(index >= min || spec.isOptional) && { shape: RenderShape.HollowCircle },
		});
	}
}

function add_autogrow_input_listeners(node: LGraphNode, specification: InputAutogrowSpecification): void {
	node.onConnectionsChange = serialize(
		node.onConnectionsChange?.bind(node),
		(type, index, connected, link, slot) => {
			const { name } = specification;

			if (NodeSlotType.INPUT !== type) {
				return;
			}

			const parsed = parse_autogrow_input_name(slot.name);
			if (name !== parsed?.name) {
				return;
			}

			expand_autogrow_inputs(node, specification);
		},
	);

	i18next.on("loaded", () => {
		update_autogrow_input_names(node, specification);
	});
}

function expand_autogrow_inputs(node: LGraphNode, specification: InputAutogrowSpecification): void {
	const {
		name,
		template: { max, min },
	} = specification;

	interface Item {
		connected: boolean;
		index: number;
		name: string;
	}

	const items = node.inputs
		.reduce<Item[]>((items, slot) => {
			const input_name = slot.name;

			const parsed = parse_autogrow_input_name(input_name);
			if (name === parsed?.name) {
				items.push({
					connected: is_node_input_connected(node, input_name),
					index: parsed.index,
					name: input_name,
				});
			}

			return items;
		}, []);

	const index_max = Math.min(
		max,
		items.reduce((index, item) => {
			if (item.connected) {
				index = Math.max(index, item.index + 1);
			}
			return index;
		}, min),
	);

	for (const item of items) {
		if (index_max < item.index) {
			remove_autogrow_input_group(node, specification, item.index);
		}
	}

	for (let index = 0; index_max >= index; index += 1) {
		add_autogrow_input_group(node, specification, index);
	}

	sort_node_inputs(node);
}

function parse_autogrow_input_name(name: string): {
	index: number;
	name: string;
} | undefined {
	const [n, suffix] = name.split("\x2E", 2);
	if (!(n && suffix)) {
		return;
	}

	const matched = (/^.+(?<index>\d+)$/u).exec(suffix)?.groups?.index;
	if (!matched) {
		return;
	}

	const index = Number(matched);
	if (!(0 <= index)) {
		return;
	}

	return {
		index,
		name: n,
	};
}

function remove_autogrow_input_group(node: LGraphNode, specification: InputAutogrowSpecification, index: number): void {
	const { input, min } = specification.template;

	if (min > index) {
		return;
	}

	for (const spec of input) {
		const name = resolve_autogrow_input_name(node, specification, input, spec, index)?.name;
		if (name) {
			remove_node_input(node, name);
		}
	}
}

function resolve_autogrow_input_name(
	node: LGraphNode,
	specification: InputAutogrowSpecification,
	input_specifications: InputAutogrowSpecification["template"]["input"],
	input_specification: InputAutogrowSpecification["template"]["input"][number],
	index: number,
): {
	localized_name: string;
	name: string;
} | undefined {
	const definition = get_node_definition(node);
	if (!definition) {
		return;
	}

	const t = create_node_input_translation(definition, specification);

	const { names } = specification.template;

	if (names) {
		const name = names[index];
		if (!name) {
			return;
		}

		return {
			localized_name: t(`template.names.${index}`, { defaultValue: name }),
			name,
		};
	}

	if (1 === input_specifications.length) {
		const {
			name,
			template: { prefix },
		} = specification;
		if (!prefix) {
			return;
		}

		return {
			localized_name: `${t("template.prefix", { defaultValue: prefix })}${index}`,
			name: `${name}.${prefix}${index}`,
		};
	}

	const { name } = specification;
	const { name: input_name } = input_specification;

	return {
		localized_name: `${t(`template.inputs.${input_name}.name`, { defaultValue: input_name })}${index}`,
		name: `${name}.${input_name}${index}`,
	};
}

function setup_node_input(node: LGraphNode, specification: InputAutogrowSpecification): void {
	remove_node_input(node, specification.name);
	expand_autogrow_inputs(node, specification);
	add_autogrow_input_listeners(node, specification);
}

function update_autogrow_input_names(node: LGraphNode, specification: InputAutogrowSpecification): void {
	const { input } = specification.template;

	for (const slot of node.inputs) {
		const parsed = parse_autogrow_input_name(slot.name);
		if (!parsed) {
			continue;
		}

		for (const spec of input) {
			const localized_name = resolve_autogrow_input_name(node, specification, input, spec, parsed.index)?.localized_name;
			slot.localized_name = localized_name;
		}
	}
}

app.registerExtension({
	name: "One.Widget.Autogrow",
	beforeRegisterNodeDef: (_, definition) => {
		foreach_node_input_specification(
			definition.input,
			(specification) => "COMFY_AUTOGROW_V3" === specification.type,
			(_, specification) => {
				specification[0] = "ONE_AUTOGROW";
			},
		);
	},
	getCustomWidgets: () => {
		return {
			ONE_AUTOGROW: (node, name, data) => {
				const specification = transform_node_input_specification(name, data) as InputSpec & z.infer<typeof zAutogrowOptions>;

				const { template } = specification;
				const {
					input,
					max,
					min = 0,
					names,
				} = template;

				const one = ("@one" in template ? template["@one"] : undefined) as { max?: number } | undefined;

				const spec = {
					...specification,
					template: {
						...template,
						input: transform_node_input_specifications(input),
						max: names?.length ?? Math.max(min, (one ? one.max : max) ?? Infinity),
						min,
					},
				};

				setup_node_input(node, spec);
			},
		};
	},
	nodeCreated: (node) => {
		foreach_node_input_specification(
			get_node_definition(node)?.input,
			(specification) => "ONE_AUTOGROW" === specification.type,
			(specification) => {
				remove_node_input(node, specification.name);
			},
		);
	},
});
