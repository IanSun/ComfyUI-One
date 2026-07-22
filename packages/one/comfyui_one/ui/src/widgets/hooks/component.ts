import type { DOMWidgetProps } from "../../internal/node";

import { useStore } from "@nanostores/react";
import { useCallback, useMemo } from "react";

export function useValueProps<T, V = T>({
	parse,
	serialize,
	store,
	widget,
}: {
	parse?: (value: T) => V;
	serialize?: (value: V) => T;
} & Pick<DOMWidgetProps<T>, "store" | "widget">): {
	onChange: (value: null | undefined | V) => void;
	value: undefined | V;
} {
	const serialized_value = useStore(store);

	const value = useMemo(() => {
		if ("undefined" === typeof serialized_value || null === serialized_value) {
			return;
		}

		if (parse) {
			try {
				return parse(serialized_value);
			}
			catch {}
		}

		return serialized_value as V;
	}, [parse, serialized_value]);

	const onChange = useCallback((value: null | undefined | V) => {
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
	}, [serialize, widget]);

	return {
		onChange,
		value,
	};
}
