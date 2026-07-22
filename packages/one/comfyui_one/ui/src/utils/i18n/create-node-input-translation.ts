import type { ComfyNodeDef } from "@comfyorg/object-info-parser";
import type { InputSpec } from "@comfyorg/object-info-parser/schemas/nodeDefSchemaV2";
import type { TFunction } from "i18next";

import i18next from "i18next";

export const create_node_input_translation = (
	definition: ComfyNodeDef,
	specification: InputSpec,
): TFunction<"nodeDefs", `${string}.inputs.${string}`> => {
	return i18next.getFixedT(null, "nodeDefs", `${definition.name}.inputs.${specification.name}`);
};
