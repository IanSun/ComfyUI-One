import type { ComponentProps } from "react";

import { cn } from "cn";
import { memo } from "react";
import { TextArea as TextAreaPrimitive } from "react-aria-components";

export const Textarea = memo(({
	className,
	...props
}: ComponentProps<typeof TextAreaPrimitive>) => {
	return <TextAreaPrimitive
		className={cn(
			"field-sizing-content resize-y min-h-16 w-full min-w-0 rounded-md border-none bg-component-node-widget-background p-1.5 px-1.5 text-component-node-foreground text-xs outline-none ring-0 ring-component-node-widget-background/0 shadow-none focus:ring focus:ring-component-node-widget-background-hovered focus:shadow-xs transition-shadow cursor-auto",
			className,
		)}
		data-slot="textarea"
		{...props}
	/>;
});

export const TextareaSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof Textarea>, "className">) => {
	return <div
		className={cn(
			"min-h-16 w-full min-w-0 rounded-md bg-component-node-widget-background p-1.5 px-1.5 cursor-auto",
			className,
		)}
		data-slot="textarea"
	>
		<div className="flex h-4 items-center">
			<div className="h-1.5 w-full rounded-full bg-component-node-foreground/40" />
		</div>
		<div className="flex h-4 items-center">
			<div className="h-1.5 w-24 max-w-1/2 rounded-full bg-component-node-foreground/40" />
		</div>
	</div>;
});
