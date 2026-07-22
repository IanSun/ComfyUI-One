import type { DOMWidget } from "@/types";
import type { ComfyNodeDef } from "@comfyorg/object-info-parser";
import type { InputSpec } from "@comfyorg/object-info-parser/schemas/nodeDefSchemaV2";
import type { Atom } from "nanostores";

import { createContext, use } from "react";

export interface DOMWidgetContextValue<T, U> {
	definition: ComfyNodeDef;
	specification: InputSpec & U;
	store: Atom<T | undefined>;

	/** @ts-expect-error */
	widget: DOMWidget<HTMLDivElement, T>;
}

export const NodeDOMWidgetContext = createContext<DOMWidgetContextValue<unknown, object> | null>(null);

export function useNodeDOMWidgetContext<T = unknown, U = object>(): DOMWidgetContextValue<T, U> {
	return use(NodeDOMWidgetContext) as DOMWidgetContextValue<T, U>;
}
