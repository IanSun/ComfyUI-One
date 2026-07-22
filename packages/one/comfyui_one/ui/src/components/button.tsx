import type { ComponentProps } from "react";

import { cn } from "cn";
import { memo } from "react";
import { Button as ButtonPrimitive } from "react-aria-components";

export const Button = memo(({
	className,
	size = "default",
	variant = "default",
	...props
}: {
	size?: "default" | "icon";
	variant?: "default" | "ghost";
} & ComponentProps<typeof ButtonPrimitive>) => {
	return <ButtonPrimitive
		className={cn(
			"group/button shrink-0 inline-flex data-[size=icon]:size-6 rounded-md border border-transparent bg-clip-padding bg-transparent data-[variant=ghost]:bg-component-node-widget-background/0 shadow-none data-[variant=ghost]:hover:bg-component-node-widget-background-hovered data-[variant=ghost]:focus:bg-component-node-widget-background-hovered data-[variant=ghost]:pressed:bg-component-node-widget-background-selected p-0 items-center justify-center text-component-node-foreground data-[variant=ghost]:disabled:text-component-node-foreground/40 text-xs truncate data-[variant=ghost]:hover:shadow-xs data-[variant=ghost]:focus:shadow-xs data-[variant=ghost]:pressed:shadow-xs outline-none transition-[background-color,box-shadow,color] select-none cursor-auto [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-3 [&_svg]:pointer-events-none",
			className,
		)}
		data-size={size}
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
			"group/button shrink-0 inline-flex rounded-md border border-transparent items-center justify-center text-component-node-foreground/40 select-none cursor-auto [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-3 [&_svg]:pointer-events-none",
			className,
		)}
		data-slot="button"
		data-variant={variant}
		{...props}
	/>;
});
