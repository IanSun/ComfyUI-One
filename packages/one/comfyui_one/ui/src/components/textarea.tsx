import type { HTMLProps } from "@base-ui/react";
import type { ComponentProps, FunctionComponent } from "react";

import { Input as InputPrimitive, mergeProps } from "@base-ui/react";
import { memo, useCallback, useMemo } from "react";

export const Textarea = memo(({
	className,
	...props
}: InputPrimitive.Props) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<InputPrimitive.Props, "className">>>(
			{ className },
			{ className: "one:placeholder:text-muted-foreground" },
			{ className: "one:block one:min-h-20 one:h-20 one:w-full one:resize-y one:rounded-lg one:border-none one:bg-background one:py-2 one:px-3 one:text-sm one:text-current one:outline one:outline-solid one:-outline-offset-1 one:outline-input one:focus-visible:outline-ring one:ring-0 one:focus-visible:ring-3 one:ring-ring/0 one:focus-visible:ring-ring/50 one:outline-none one:disabled:opacity-50 one:transition-[background-color,box-shadow,opacity,outline-color] one:select-none one:cursor-auto" },
		),
		[className],
	));

	const render = useCallback((props: HTMLProps) => <textarea {...props} />, []);

	return <InputPrimitive
		className={className}
		render={render}
		{...props}
	/>;
});

export const TextareaSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div">) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComponentProps<"div">, "className">>>(
			{ className },
			{ className: "one:after:flex-none one:after:block one:after:h-3.5 one:after:w-6/10 one:after:rounded-md one:after:bg-muted" },
			{ className: "one:before:flex-none one:before:block one:before:h-3.5 one:before:w-full one:before:rounded-md one:before:bg-muted" },
			{ className: "one:flex one:flex-col one:h-20 one:w-full one:rounded-lg one:bg-muted/30 one:py-2.75 one:px-3 one:gap-1.5 one:animate-pulse one:select-none one:pointer-events-none one:cursor-auto" },
		),
		[className],
	));

	return <div
		className={className}
		{...props}
	/>;
});
