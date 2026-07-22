import { useCallback } from "react";
import { useNodeDOMWidgetContext } from "./useNodeDOMWidgetContext";

export function useNodeDOMWidgetOnValueChange<T, V = T>(serialize?: (value: V) => T): (value: null | undefined | V) => void {
	const { widget } = useNodeDOMWidgetContext<T>();

	return useCallback((value: null | undefined | V) => {
		if ("undefined" === typeof value || null === value) {
			return;
		}

		if (serialize) {
			try {
				widget.value = serialize(value);
			}
			catch {}
		}
		else {
			widget.value = value as T;
		}
	}, [widget, serialize]);
}
