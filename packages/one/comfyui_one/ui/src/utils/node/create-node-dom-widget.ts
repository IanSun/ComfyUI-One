import type { DOMWidgetContextValue } from "../../hooks/useNodeDOMWidgetContext";
import type { LGraphNode } from "@/lib/litegraph/src/litegraph";
import type { DOMWidget as ComfyDOMWidget } from "@/types";
import type { InputSpec } from "@comfyorg/object-info-parser/schemas/nodeDefSchemaV2";
import type { ElementType, FC, ReactNode } from "react";

import { atom } from "nanostores";
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { Widget } from "../../components";
import { serialize } from "../common";
import { get_node_definition } from "./get-node-definition";

/** @ts-expect-error */
export type DOMWidget<T> = ComfyDOMWidget<HTMLDivElement, T>;

export function create_node_dom_widget<T, U = object>(
	node: LGraphNode,
	name: string,
	type: string,
	specification: InputSpec & U,
	component: ElementType,
): DOMWidget<T> | undefined {
	const definition = get_node_definition(node);
	if (!definition) {
		return;
	}

	const store = atom(specification.default as T | undefined);
	const element = document.createElement("div");
	element.classList.add("relative");

	/** @ts-expect-error */
	const widget = node.addDOMWidget<HTMLDivElement, T>(name, type, element, {
		getValue: () => {
			return store.get();
		},
		setValue: (value) => {
			store.set(value);
		},
	});
	widget.onRemove = serialize(
		widget.onRemove?.bind(widget),
		() => {
			root.unmount();
		},
	);

	const root = createRoot(element);
	root.render(
		createElement(Widget as FC<{ children?: ReactNode } & DOMWidgetContextValue<T, U>>, {
			children: createElement(component),
			definition,
			specification,
			store,
			widget,
		}),
	);

	return widget;
}
