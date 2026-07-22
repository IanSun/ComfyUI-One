import type { ComponentProps } from "react";

import { cn } from "cn";
import { memo } from "react";
import { Label as LabelPrimitive } from "react-aria-components";

export const Label = memo(({
	className,
	...props
}: ComponentProps<typeof LabelPrimitive>) => {
	return <LabelPrimitive
		className={cn(
			"flex items-center text-xs leading-none select-none cursor-auto",
			className,
		)}
		data-slot="label"
		{...props}
	/>;
});

export const LabelSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof Label>, "className">) => {
	return <div
		className={cn(
			"flex items-center select-none cursor-auto",
			className,
		)}
		data-slot="label"
	>
		<div className="h-1.5 w-16 max-w-full rounded-full bg-component-node-foreground/40" />
	</div>;
});
