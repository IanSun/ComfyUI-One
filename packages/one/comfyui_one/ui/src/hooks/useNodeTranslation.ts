import type { TFunction } from "i18next";

import i18next from "i18next";
import { useTranslation } from "react-i18next";
import { useNodeDOMWidgetContext } from "./useNodeDOMWidgetContext";

export function useNodeTranslation(): TFunction<"nodeDefs", string> {
	const { definition } = useNodeDOMWidgetContext();

	const { t } = useTranslation("nodeDefs", {
		i18n: i18next,
		keyPrefix: definition.name,
	});

	return t;
}
