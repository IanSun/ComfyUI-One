import type { ComfyNodeDef, InputSpec as InputSpecV1 } from "@comfyorg/object-info-parser";
import type { InputSpec as InputSpecV2 } from "@comfyorg/object-info-parser/schemas/nodeDefSchemaV2";

import { transform_node_input_specification } from "./transform-node-input-specification";

export function find_node_input_specification(
	input: ComfyNodeDef["input"],
	predicate: (specification: InputSpecV2, specification_1: InputSpecV1) => boolean,
): InputSpecV1 | undefined;
export function find_node_input_specification(
	input: ComfyNodeDef["input"],
	predicate: (specification: InputSpecV2, specification_1: InputSpecV1) => boolean,
	transform: true,
): InputSpecV2 | undefined;
export function find_node_input_specification(
	input: ComfyNodeDef["input"],
	predicate: (specification: InputSpecV2, specification_1: InputSpecV1) => boolean,
	transform?: true,
): InputSpecV1 | InputSpecV2 | undefined {
	for (const [index, record = {}] of [input?.required, input?.optional].entries()) {
		for (const [name, specification_1] of Object.entries(record)) {
			const specification = transform_node_input_specification(name, specification_1, 1 === index);

			if (predicate(specification, specification_1)) {
				return transform ? specification : specification_1;
			}
		}
	}
}
