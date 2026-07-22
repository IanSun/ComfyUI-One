import type { ComponentProps } from "react";
import type { InputProps as InputPrimitiveProps } from "react-aria-components";

import { cn } from "cn";
import { memo } from "react";
import { Input as InputPrimitive } from "react-aria-components";

export const Input = memo(({
	className,
	type,
	...props
}: InputPrimitiveProps) => {
	return <InputPrimitive
		className={cn(
			"h-6 w-full min-w-0 rounded-md border-none bg-component-node-widget-background p-0 px-1.5 text-current text-xs outline-none focus:ring focus:ring-component-node-widget-background-highlighted focus-visible:ring focus-visible:ring-component-node-widget-background-highlighted cursor-auto",
			className,
		)}
		data-slot="input"
		type={type}
		{...props}
	/>;
});

export const InputSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof Input>, "className">) => {
	return <div
		className={cn(
			"flex h-6 w-full min-w-0 rounded-md bg-component-node-widget-background px-1.5 items-center cursor-auto",
			className,
		)}
		data-slot="input"
	>
		<div className="h-1.5 w-24 max-w-1/2 rounded-full bg-current/40" />
	</div>;
});
