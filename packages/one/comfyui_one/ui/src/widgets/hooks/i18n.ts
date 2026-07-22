import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef } from "@/schemas/nodeDefSchema";
import type { TFunction } from "i18next";

import i18next from "i18next";
import { useTranslation } from "react-i18next";

export const useNodeTranslation = (definition: ComfyNodeDef): TFunction<"nodeDefs", string> => {
	const { t } = useTranslation("nodeDefs", {
		i18n: i18next,
		keyPrefix: definition.name,
	});

	return t;
};

export const useNodeInputTranslation = (
	definition: ComfyNodeDef,
	specification: InputSpec,
): TFunction<"nodeDefs", `${string}.inputs.${string}`> => {
	const { t } = useTranslation("nodeDefs", {
		i18n: i18next,
		keyPrefix: `${definition.name}.inputs.${specification.name}`,
	});

	return t;
};
