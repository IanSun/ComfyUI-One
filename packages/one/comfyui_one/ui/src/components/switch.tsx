import type { ComponentProps } from "react";

import { cn } from "cn";
import { memo } from "react";
import { SwitchButton as SwitchButtonPrimitive } from "react-aria-components";

export const Switch = memo(({
	className,
	...props
}: ComponentProps<typeof SwitchButtonPrimitive>) => {
	return <SwitchButtonPrimitive
		className={cn(
			"group/switch peer shrink-0 inline-flex h-6 rounded-full items-center select-none cursor-auto",
			className,
		)}
		data-slot="switch"
		{...props}
	>
		<div
			className="flex h-4 w-8 rounded-full bg-component-node-widget-background group-selected/switch:bg-primary-background items-center ring-0 ring-component-node-widget-background/0 group-focus/switch:ring group-focus/switch:ring-component-node-widget-background-hovered transition-[background-color,box-shadow]"
			data-slot="switch-track"
		>
			<div
				className="size-3 rounded-full bg-component-node-foreground translate-x-0.5 group-selected/switch:translate-x-4.5 transition-transform pointer-events-none"
				data-slot="switch-thumb"
			/>
		</div>
	</SwitchButtonPrimitive>;
});

export const SwitchSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof Switch>, "className">) => {
	return <div
		className={cn(
			"group/switch peer shrink-0 inline-flex h-6 rounded-full items-center select-none cursor-auto",
			className,
		)}
		data-slot="switch"
	>
		<div
			className="flex h-4 w-7.5 rounded-full bg-component-node-widget-background items-center"
			data-slot="switch-track"
		>
			<div
				className="size-3 rounded-full bg-component-node-foreground translate-x-0.5 pointer-events-none"
				data-slot="switch-thumb"
			/>
		</div>
	</div>;
});
