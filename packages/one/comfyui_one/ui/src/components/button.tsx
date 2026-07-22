import type { ComponentProps } from "react";
import type { ButtonProps as ButtonPrimitiveProps } from "react-aria-components";

import { cn } from "cn";
import { memo } from "react";
import { Button as ButtonPrimitive } from "react-aria-components";

export const Button = memo(({
	className,
	variant = "default",
	...props
}: { variant?: "default" | "ghost" } & ButtonPrimitiveProps) => {
	return <ButtonPrimitive
		className={cn(
			"group/button shrink-0 inline-flex rounded-md border border-transparent bg-clip-padding bg-transparent data-[variant=ghost]:hover:bg-component-node-widget-background-hovered p-0 items-center justify-center text-current text-xs whitespace-nowrap outline-none transition-colors select-none cursor-auto [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 [&_svg]:pointer-events-none",
			className,
		)}
		data-slot="button"
		data-variant={variant}
		{...props}
	/>;
});

export const ButtonSkeleton = memo(({
	className,
	variant = "default",
	...props
}: ComponentProps<"div"> & Pick<ComponentProps<typeof Button>, "className" | "variant">) => {
	return <div
		className={cn(
			"group/button shrink-0 inline-flex rounded-md border border-transparent items-center justify-center text-current/40 select-none cursor-auto [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 [&_svg]:pointer-events-none",
			className,
		)}
		data-slot="button"
		data-variant={variant}
		{...props}
	/>;
});
