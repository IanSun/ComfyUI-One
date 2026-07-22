import type { ComponentProps } from "react";
import type { TextAreaProps as TextAreaPrimitiveProps } from "react-aria-components";

import { cn } from "cn";
import { memo } from "react";
import { TextArea as TextAreaPrimitive } from "react-aria-components";

export const Textarea = memo(({
	className,
	...props
}: TextAreaPrimitiveProps) => {
	return <TextAreaPrimitive
		className={cn(
			"field-sizing-content resize-y min-h-16 w-full min-w-0 rounded-md border-none bg-component-node-widget-background p-1.5 px-1.5 text-current text-xs outline-none focus:ring focus:ring-component-node-widget-background-highlighted focus-visible:ring focus-visible:ring-component-node-widget-background-highlighted cursor-auto",
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
			<div className="h-1.5 w-full rounded-full bg-current/40" />
		</div>
		<div className="flex h-4 items-center">
			<div className="h-1.5 w-24 max-w-1/2 rounded-full bg-current/40" />
		</div>
	</div>;
});
