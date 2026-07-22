import type { InputSpec as InputSpecV1 } from "@comfyorg/object-info-parser";
import type { InputSpec as InputSpecV2 } from "@comfyorg/object-info-parser/schemas/nodeDefSchemaV2";

export function transform_node_input_specification(
	name: string,
	specification: InputSpecV1,
	optional = false,
): InputSpecV2 {
	return {
		isOptional: optional,
		name,
		type: ((type) => "string" === typeof type ? type : "UNKNOWN")(specification[0]),
		...specification[1],
	};
}
