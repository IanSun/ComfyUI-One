import type { Context, ReactNode } from "react";

import { createElement } from "react";

export const Provider = <T extends readonly unknown[]>({
	children,
	value,
}: {
	children?: ReactNode;
	value: {
		[K in keyof T]: readonly [Context<T[K]>, T[K]];
	};
}): ReactNode => {
	if (children) {
		for (const [context, context_value] of value) {
			children = createElement(
				context,
				{ value: context_value },
				children,
			);
		}

		return children;
	}

	return null;
};
