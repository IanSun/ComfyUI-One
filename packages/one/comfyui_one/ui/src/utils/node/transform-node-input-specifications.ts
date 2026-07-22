import type { ComfyNodeDef } from "@comfyorg/object-info-parser";
import type { InputSpec } from "@comfyorg/object-info-parser/schemas/nodeDefSchemaV2";

import { transform_node_input_specification } from "./transform-node-input-specification";

export function transform_node_input_specifications(input: ComfyNodeDef["input"]): InputSpec[] {
	return [input?.required, input?.optional].flatMap((record = {}, index) => {
		return Object.entries(record).map(([name, specification]) => {
			return transform_node_input_specification(name, specification, 1 === index);
		});
	});
}
