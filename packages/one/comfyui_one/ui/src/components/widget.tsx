import type { DOMWidgetContextValue } from "../hooks/useNodeDOMWidgetContext";
import type { FC, ReactNode } from "react";

import { NodeDOMWidgetContext } from "../hooks/useNodeDOMWidgetContext";

export const Widget: FC<{ children?: ReactNode } & DOMWidgetContextValue<unknown, unknown>> = ({
	children,
	...props
}) => {
	return <NodeDOMWidgetContext
		children={children}
		value={props}
	/>;
};
