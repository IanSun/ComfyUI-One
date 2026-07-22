import type { ComfyNodeDef } from "@comfyorg/object-info-parser";
import type { TFunction } from "i18next";

import i18next from "i18next";

export const create_node_translation = (definition: ComfyNodeDef): TFunction<"nodeDefs", string> => {
	return i18next.getFixedT(null, "nodeDefs", definition.name);
};
