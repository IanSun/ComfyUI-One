import type { ComponentProps } from "react";

import { cn } from "cn";
import { memo } from "react";
import { Separator as SeparatorPrimitive } from "react-aria-components";

export const Separator = memo(({
	className,
	orientation = "horizontal",
	...props
}: ComponentProps<typeof SeparatorPrimitive>) => {
	return <SeparatorPrimitive
		className={cn(
			"shrink-0 block [:is(hr)]:h-px [:is(hr)]:w-full rounded-full border-none bg-component-node-border/10",
			className,
		)}
		data-slot="separator"
		orientation={orientation}
		{...props}
	/>;
});
