import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef } from "@/schemas/nodeDefSchema";
import type { TFunction } from "i18next";

import i18next from "i18next";

export const create_node_translation = (definition: ComfyNodeDef): TFunction<"nodeDefs", string> => {
	return i18next.getFixedT(null, "nodeDefs", definition.name);
};

export const create_node_input_translation = (
	definition: ComfyNodeDef,
	specification: InputSpec,
): TFunction<"nodeDefs", `${string}.inputs.${string}`> => {
	return i18next.getFixedT(null, "nodeDefs", `${definition.name}.inputs.${specification.name}`);
};
