import { useStore } from "@nanostores/react";
import { useMemo } from "react";
import { useNodeDOMWidgetContext } from "./useNodeDOMWidgetContext";

export function useNodeDOMWidgetValue<T, V = T>(parse?: (value: T) => V): undefined | V {
	const { store } = useNodeDOMWidgetContext<T>();

	const value = useStore(store);

	return useMemo(() => {
		if ("undefined" === typeof value) {
			return;
		}

		if (parse) {
			try {
				return parse(value);
			}
			catch {}
		}
		else {
			return value as V;
		}
	}, [value, parse]);
}
